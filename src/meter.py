import numpy as np
import re
import pronouncing
from string import punctuation


def get_word_scansion(word):
    """
    Get the scansion per word, as a string of 0's and 1's.

    Example:

    > get_word_scansion('television')
    > '1010'
    """
    word = word.strip(punctuation)
    if word == "":
        return ""
    pronounciation = pronouncing.phones_for_word(word)
    if pronounciation:
        stresses = pronouncing.stresses(pronounciation[0])
    else:
        word = re.sub("'.+", "", word)
        pronounciation = pronouncing.phones_for_word(word)
        if pronounciation:
            stresses = pronouncing.stresses(pronounciation[0])
        else:
            stresses = "?"
    return re.sub("2", "1", stresses)


def get_line_scansion(line):
    """
    Get the scansion per line, as a string of 0's and 1's.

    Example:

    > get_line_scansion("I love poetry")
    > '11100'

    """
    return "".join([get_word_scansion(word) for word in line.split(" ")])


def get_syllables_per_line_combined(combined_lines, n_syllables_per_line):
    """
    Takes as input a list of tuples and calculates the line lengths based on the combined lines.
    combined_lines: A list of tuples, in which the elements of the tuples are indices to the list n_syllables_per_line
    n_syllables_per_line: A list with numerical values, denoting the number of syllables per line.

    Example:

    > get_syllables_per_line_combined([(0,), (1,), (2,3,)], [1,2,3,4])
    > [1, 2, 7]
    """
    return [sum([n_syllables_per_line[i] for i in tpl]) for tpl in combined_lines]


def combine_line_scansions(scansion_list):
    """
    Returns a list of tuples suggesting which lines to combine based on the number of syllables.
    It aims to create as many lines as possible with length equal to the two longest line lenghts.

    For example, with as input the following scansion list;

    ['11101001011',
     '11101011001',
     '111011',
     '11011']

     the function will return [(0,), (1,), (2,3,)] since it could be transformed into

     ['11101001011',
      '11101011001',
      '11101111011']

    """
    # Count syllables per line
    n_syllables_per_line = [len(x) for x in scansion_list]
    combined_lines = [tuple([x]) for x in range(len(n_syllables_per_line)) if n_syllables_per_line[x] > 0]
    n_syllables_per_line_combined = get_syllables_per_line_combined(combined_lines, n_syllables_per_line)
    unique_line_lengths = sorted(np.unique(np.array(n_syllables_per_line_combined)), key=lambda item: -item)
    target_line_lengths = unique_line_lengths[: np.min([len(unique_line_lengths), 2])]

    improvement_found = True
    while improvement_found:

        # Find out if any two, three or four lines can be combined in order to create a new line that
        # has the same amount of syllables as any of the two longest lines in the poem.
        n_syllables_per_line_combined = get_syllables_per_line_combined(combined_lines, n_syllables_per_line)
        for target_length in target_line_lengths:
            for n_lines_to_combine in [2, 3, 4]:  # try to combine 2,3 or 4 lines.
                idx_start = []
                if n_lines_to_combine < len(n_syllables_per_line_combined):
                    combined_line_lengths = np.convolve(
                        n_syllables_per_line_combined,
                        np.ones(n_lines_to_combine, dtype=int),
                        "valid",
                    )
                    idx_start = np.where(combined_line_lengths == target_length)[0]
                    if len(idx_start) > 0:
                        break
            if len(idx_start) > 0:
                break

        # If any lines can be combined, merge the tuples of these two lines in the list combined_lines
        if len(idx_start) > 0:
            idx_lines_to_combine = list(range(idx_start[0], (idx_start[0] + n_lines_to_combine)))
            new_tpl = tuple([x for i in idx_lines_to_combine for x in combined_lines[i]])
            combined_lines[idx_start[0]] = new_tpl
            del combined_lines[(idx_start[0] + 1) : (idx_start[0] + n_lines_to_combine)]
        else:
            improvement_found = False

    return combined_lines


def merge_lines(lines, tuple_list, sep=""):
    """
    combines elements from 'lines' according to the logic defined in 'tuple_list'

    Example:

    tuple_list = [(1,), (2,3,)]
    lines = ['a','b','c','d']
    > merge_lines(lines,tuple_list)
    > ['b', 'cd']
    """
    return [sep.join([lines[a] for a in tpl]) for tpl in tuple_list]


def scansion_match_score(found_meter, known_meter):
    """
    Count the number of places where the known and found meter both are unstressed, i.e. have a '0'.
    Also add the number of 1's predicted correctly divded by the number of 1's in the known meter.
    Substract eps to make sure that correctly predicted 0's is always prioritized, and the 1's are only
    used to determine ties.

    Example:
    > scansion_match_score('1010','0010')
    > 2.99999

    """

    eps = 0.00001
    matching_0 = sum((found_meter[i] == "0") and (known_meter[i] == "0") for i in range(len(found_meter)))
    matching_1 = sum((found_meter[i] == "1") and (known_meter[i] == "1") for i in range(len(found_meter)))
    matching_1_frac = matching_1 / sum((x == "1" for x in known_meter)) - eps

    return matching_0 + matching_1_frac


def get_known_meter(scansion_list, known_meters_inv):
    """
    Use a list of scansion per line to estimate the meter of the poem. The assumption is
    that a poem always has at most two different known meters. Furthermore, since our method of
    identifying the scansion overestimates the number of stressed syllables, we will use the number
    of accurate non-stressed syllables to determine the known meter. If the number of unstressed syllables
    is equal, we look at the correct stressed syllables.

    scansion_list: A list with scansions per line, denoted as a string with 1's and 0's.
    known_meters_inv: A dict with keys strings of scansions, and as values the corresponding meter name.

    Example usage:
    > known_meters_inv = {'1010' : 'trochaic bimeter',
    >                     '101' :  'trochaic bimeter*'}
    > scansion_list = ['1010','1010','1011','1010']
    > get_known_meter(scansion_list, known_meters_inv)
    > ['trochaic bimeter']

    """
    scansion_list = [x for x in scansion_list if "?" not in x]

    # First, create meter_list; a list which elements have the structure [a,b] where a is the number
    # of syllables in the line, and b a list of the most likely know meters.
    meter_list = []
    for scansion in scansion_list:
        l = [(scansion_match_score(scansion, k), v) for k, v in known_meters_inv.items() if len(k) == len(scansion)]
        if l:
            maxValue = max(l, key=lambda x: x[0])[0]
            maxValueList = [x[1] for x in l if x[0] == maxValue]
            meter_list.append([len(scansion), maxValueList])

    # If meter_list has at least one element, create meters_list. The elements in this list
    # contain per line length all the predicted meters, still to be flattened.
    # If more than two elements, we only look at the stats for the two most common line lengths.
    if meter_list:
        (values, counts) = np.unique([x[0] for x in meter_list], return_counts=True)
        values = values[counts > 1]
        counts = counts[counts > 1]
        values = values[(-counts).argsort()][: np.min([len(values), 2])]
        meters_list = [[y[1] for y in meter_list if y[0] == val] for val in values]

        # Now, find per line length the most commonly predicted meter. In case of a tie, pick one at random.
        # Sorry, best we can do for now...
        result = list()
        for meters_per_line_length in meters_list:
            flat_list = [item for sublist in meters_per_line_length for item in sublist]
            (values, counts) = np.unique(flat_list, return_counts=True)
            ind = np.where(counts == np.max(counts))
            if len(ind[0]) > 1:
                result.append(np.random.choice(values[ind]))
            else:
                result.append(values[ind][0])
        result.sort()
    else:
        result = "unknown"
    return result
