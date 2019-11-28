import os
import datetime as dt
import re
import json
import pandas as pd

from src.reddit_user_comment_reader import RedditUserCommentReader
from src.string import clean_comment


def load_data(json_filepath,verbose=False):
    """ 
    Load the dataset. If the json file with comments by /u/poem_for_your_sprog is more than 24 hours old,
    use the RedditUserCommentReader class to download the new dataset.
    """
    
    if verbose: print('Loading data...')
    download_comments = True
    if os.path.isfile(json_filepath):
        if verbose: print('Existing file found!')
        mtime = os.path.getmtime(json_filepath)
        if verbose: print("last modified: %s" % dt.datetime.fromtimestamp(mtime))
        if (dt.datetime.now() - dt.datetime.fromtimestamp(mtime)).days < 1: # if modified in last 24 hours
            download_comments = False

    if download_comments:
        if verbose: print('Downloading comments...')
        reddit_user_comment_reader = RedditUserCommentReader('poem_for_your_sprog', verbose = True)
        all_comments = reddit_user_comment_reader.get_comments()
        if verbose: print('Saving to file...')
        with open(json_filepath, 'w') as outfile:
            json.dump(all_comments, outfile)
    else:   
        if verbose: print('Loading comments from file...')
        with open(json_filepath, 'r') as infile:
            all_comments = json.load(infile)
    if verbose: print('Done.')

    df = pd.DataFrame(all_comments)
    df = df[df['author']!='[deleted]']
    df['poem'] = df['body'].apply(clean_comment)
    df['datetime'] = df['created_utc'].apply(dt.datetime.fromtimestamp)
    df['date'] = df['datetime'].dt.date
    df['awards_simple'] = df['all_awardings'].apply(lambda x: [y['name'] + ': ' + str(y['count']) for y in x]) 
    df['number_of_lines'] = df['poem'].apply(lambda x: 1+ sum(1 for _ in re.finditer(r'>', x)))
    df['comment_length']= df['poem'].str.len()
    df['average_line_length'] = df['comment_length']/(df['number_of_lines'])
    # Try to determine if comment or poem.
    df['type'] = 'poem'
    df.loc[df['date']!=dt.date(2015,6,23),'type'] ='comment' # AMA
    df.loc[df['poem'].apply(len)>0,'type'] = 'comment'
    df.loc[df['number_of_lines']>1,'type'] = 'comment'
    df.loc[df['average_line_length']<55,'type'] = 'comment'
    return df