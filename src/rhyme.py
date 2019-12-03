import re

def get_last_word(line):
    """
    Returns the last word of a line.
    Examples:
    
    > get_last_word("This is a test. !")
    > 'test'
    
    > get_last_word("I bet you don't.")
    > "don't"
    
    """
    return re.findall(r"\s([^\.?!,\s]+)[\.?!,\s']*$",line)[0] if re.findall(r"\s([^\.?!,\s]+)[\.?!,\s']*$",line) else None


def get_last_words_list(poem):
    """
    Returns a list of the last word for each line of a poem.
    """
    return [get_last_word(line) for line in poem.split('>')]
