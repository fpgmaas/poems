###
# Modified from a very helpful post by /u/Stuck_In_The_Matrix
# https://www.reddit.com/r/pushshift/comments/9zhj0x/how_to_get_an_archive_of_all_your_comments_from/
###

def get_comments_from_pushshift(**kwargs):
    r = requests.get("https://api.pushshift.io/reddit/comment/search/",params=kwargs)
    data = r.json()
    return data['data']

def get_comments_from_reddit_api(comment_ids,author):
    headers = {'User-agent':'Comment Collector for /u/{}'.format(author)}
    params = {}
    params['id'] = ','.join(["t1_" + id for id in comment_ids])
    r = requests.get("https://api.reddit.com/api/info",params=params,headers=headers)
    data = r.json()
    return data['data']

class RedditUserCommentReader():
    
    def __init__(self,user: str, verbose: bool = False):
        self.user = user
        self.verbose = verbose
    
    def get_comments(self):
        all_comments = list()
        before = None
        while True:
            comments = get_comments_from_pushshift(author=self.user,
                                                   size=100,
                                                   before=before,
                                                   sort='desc',
                                                   sort_type='created_utc')
            if not comments: break

            # This will get the comment ids from Pushshift in batches of 100 -- Reddit's API only allows 100 at a time
            comment_ids = []
            for comment in comments:
                before = comment['created_utc'] # This will keep track of your position for the next call in the while loop
                comment_ids.append(comment['id'])

            # This will then pass the ids collected from Pushshift and query Reddit's API for the most up to date information
            comments = get_comments_from_reddit_api(comment_ids,self.user)
            all_comments += [comment['data'] for comment in comments['children']]
            if self.verbose:
                print('Total number of comments fetched: {}'.format(len(all_comments)))
            time.sleep(2)
            
        return all_comments