import glob
import re
import requests
import datetime as dt
from pathlib import Path
import pandas as pd


class RedditUserCommentReader:
    def __init__(self, author: str, data_dir: str):
        self.author = author
        self.data_dir = data_dir
        self._create_data_dir_if_not_exists()

    def read(self):
        last_comment_found = False
        while not last_comment_found:
            latest_comment_utc = self._get_latest_read_comment_utc()
            comment_ids = self._get_batch_of_comment_ids_from_pushshift(from_utc=latest_comment_utc)
            if len(comment_ids) < 1:
                last_comment_found = True
            else:
                df_comments = self._get_comment_data_from_reddit_api(comment_ids)
                print(dt.datetime.fromtimestamp(int(df_comments.created_utc.max())))
                df_comments.to_pickle(
                    f"{self.data_dir}/df_{int(df_comments.created_utc.min())}_{int(df_comments.created_utc.max())}.pickle"
                )
        return self._read_all_pickle_files()

    def _create_data_dir_if_not_exists(self):
        Path(self.data_dir).mkdir(parents=True, exist_ok=True)

    def _get_batch_of_comment_ids_from_pushshift(self, from_utc):
        """
        For a list of posible arguments, see https://github.com/pushshift/api
        """
        r = requests.get(
            "https://api.pushshift.io/reddit/comment/search/",
            params={
                "author": self.author,
                "size": 100,
                "after": from_utc,
                "sort": "asc",
                "sort_type": "created_utc",
            },
        )
        data = r.json()
        return [comment["id"] for comment in data["data"]]

    def _get_comment_data_from_reddit_api(self, comment_ids):
        headers = {"User-agent": "Comment Collector for /u/{}".format(self.author)}
        params = {"id": ",".join(["t1_" + id for id in comment_ids])}
        r = requests.get("https://api.reddit.com/api/info", params=params, headers=headers)
        df = self._convert_comments_to_dataframe(r.json()["data"])
        return df

    @staticmethod
    def _convert_comments_to_dataframe(comments):
        return pd.DataFrame([comment["data"] for comment in comments["children"]])

    def _get_latest_read_comment_utc(self):
        pickle_files = [f for f in glob.glob(f"{self.data_dir}/*.pickle")]
        if len(pickle_files) < 1:
            return None
        else:
            latest_utc_per_file = [int(re.findall(r"(\d+)\.pickle", x)[0]) for x in pickle_files]
            return max(latest_utc_per_file)

    def _read_all_pickle_files(self):
        pickle_files = [f for f in glob.glob(f"{self.data_dir}/*.pickle")]
        return pd.concat([pd.read_pickle(x) for x in pickle_files])
