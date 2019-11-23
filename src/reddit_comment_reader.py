import requests
import time

def get_author_comments(**kwargs):
    # By Stuck_In_The_Matrix 
    # https://www.reddit.com/r/pushshift/comments/9xh1b1/how_would_i_get_all_users_comments/ea92d2r/
    r = requests.get("https://api.pushshift.io/reddit/comment/search/",params=kwargs)
    data = r.json()
    return data['data']

class RedditCommentReader():
    
    def __init__(self,user: str):
        self.user = user
    
    def get_comments(self):        
        all_comments = list()
        before = None
        last_comment_found = False
        
        while not last_comment_found:
            comments = get_author_comments(author=self.user,size=500,before=before,sort='desc',sort_type='created_utc')
            if comments:
                before = comments[-1]['created_utc'] 
                all_comments+=comments
            else:
                last_comment_found = True
            time.sleep(1)
            
        return all_comments