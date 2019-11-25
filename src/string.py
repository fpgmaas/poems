import re

def clean_comment(comment):
    comment = comment.lower() # Remove quoted text, often at start of a comment.
    comment = re.sub(r'&gt.+\n','',comment)
    comment = re.sub(r'(https?://\S+)',r' ',comment) # Remove URL's
    comment = re.sub(r'\n','>',comment) # Replace \n with a special character to denote linebreaks
    comment = re.sub(r'(/r/\S+)',r' ',comment) # remove links to specific subreddits
    comment = re.sub(r'[^A-Za-z0-9 >,\.!?\']', ' ', comment) # Keep only these characters
    comment = re.sub(r'amp nbsp',' ', comment) 
    comment = re.sub(r'\s([?.!",](?:\s|$))', r'\1', comment) # remove white space between text and interpunction
    comment = re.sub('\s*([>])\s*', r'\1', comment) # remove space between line breaks
    comment = re.sub(' +',' ',comment) # Remove multi-white space
    comment = re.sub('>+','>',comment) # Remove multi-linebreaks
    comment = comment.strip(' >')
    return comment