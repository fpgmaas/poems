import re
import string
import pronouncing
import numpy as np

def get_last_word(line):
    """
    Returns the last word of a line.
    Examples:
    
    > get_last_word("This is a test. !")
    > 'test'
    
    > get_last_word("I bet you don't.")
    > "don't"
    
    """
    line = line.strip(string.punctuation)
    line = line.strip()
    return re.findall(r"\s([^\.?!,\s]+)[\.?!,\s']*$",line)[0] if re.findall(r"\s([^\.?!,\s]+)[\.?!,\s']*$",line) else None


def get_last_words_list(poem):
    """
    Returns a list of the last word for each line of a poem.
    """
    return [get_last_word(line) for line in poem.split('>')]

def rhymes_all(word):
    """
    The original function prnouncing.rhymes only looks at the first (primary?) phonetical pronounciation
    to find rhyme words. This make for example 'live' only rhyme with 'five' and not with 'give'.
    This function loops over all pronounciations and finds all rhyme words, so it makes 'live' rhyme with
    both 'five' and 'give'.
    """
    phones = pronouncing.phones_for_word(word)
    if len(phones) > 0:
        return [w for phone in phones for w in pronouncing.rhyme_lookup.get(pronouncing.rhyming_part(phone), []) if w != word ]
    else:
        return []

def get_rhyme_scheme(last_words_per_line):
    """
    Convert a list of words to a rhyme scheme represented as a string, such as 'aabb' if the first two
    words rhyme, and the last two words rhyme.
    """
    alphabet = string.ascii_lowercase
    rhyme_scheme = np.empty(len(last_words_per_line),dtype=str)
    k=0
    for i in range(len(last_words_per_line)):
        if rhyme_scheme[i]=='':
            if last_words_per_line[i] is not None:
                rhyme_scheme[i]=alphabet[k % 26]
                # determine rhyming words
                rhyme_list = pronouncing.rhymes(last_words_per_line[i])          
                # if none of the rhyme words are found in the sentence, try with alternative pronounciations.        
                if not np.any([x in rhyme_list for x in last_words_per_line]):
                    rhyme_list = rhymes_all(last_words_per_line[i])  
                # find the matching rhyme words and edit the rhyme_scheme    
                if np.any([x in rhyme_list for x in last_words_per_line]):
                    rhyme_scheme[(np.array([x in rhyme_list for x in last_words_per_line]) & (rhyme_scheme == ''))] = alphabet[k % 26]
                k+=1
            else:
                rhyme_scheme[i] = '?'      
            
    return ''.join(rhyme_scheme) 
