import datetime as dt
import re


class DataFrameParser:
    def __init__(self):
        pass

    def parse(self, df):
        df = self._remove_deleted_comments(df)
        df = self._clean_comments(df)
        df = self._add_date_and_datetime(df)
        df = self._parse_awards(df)
        df = self._add_line_and_lenght_statistics(df)
        df = self._determine_comment_or_poem(df)
        return df

    @staticmethod
    def _remove_deleted_comments(df):
        return df[df["author"] != "[deleted]"]

    def _clean_comments(self, df):
        df["poem"] = df["body"].apply(self._clean_comment)
        return df

    @staticmethod
    def _add_date_and_datetime(df):
        df["datetime"] = df["created_utc"].apply(dt.datetime.fromtimestamp)
        df["date"] = df["datetime"].dt.date
        return df

    @staticmethod
    def _parse_awards(df):
        df["awards_dict"] = df["all_awardings"].apply(lambda x: {y["name"]: y["count"] for y in x})
        df["awards_simple"] = df["all_awardings"].apply(lambda x: [y["name"] + ": " + str(y["count"]) for y in x])
        return df

    @staticmethod
    def _add_line_and_lenght_statistics(df):
        df["number_of_lines"] = df["poem"].apply(lambda x: 1 + sum(1 for _ in re.finditer(r">", x)))
        df["comment_length"] = df["poem"].str.len()
        df["average_line_length"] = df["comment_length"] / (df["number_of_lines"])
        return df

    @staticmethod
    def _determine_comment_or_poem(df):
        df["type"] = "poem"
        df.loc[df["date"] == dt.date(2015, 6, 23), "type"] = "comment"  # AMA
        df.loc[df["poem"].apply(len) < 1, "type"] = "comment"
        df.loc[df["number_of_lines"] <= 1, "type"] = "comment"
        df.loc[df["average_line_length"] >= 55, "type"] = "comment"
        return df

    @staticmethod
    def _clean_comment(comment):
        comment = comment.lower()  # Remove quoted text, often at start of a comment.
        comment = re.sub(r"&gt.+\n", "", comment)
        comment = re.sub(r"(https?://\S+)", r" ", comment)  # Remove URL's
        comment = re.sub(r"\n", ">", comment)  # Replace \n with a special character to denote linebreaks
        comment = re.sub(r"(/r/\S+)", r" ", comment)  # remove links to specific subreddits
        comment = re.sub(r"[^A-Za-z0-9 >,\.!?\'-]", " ", comment)  # Keep only these characters
        comment = re.sub(r"amp nbsp", " ", comment)
        comment = re.sub(r'\s([?.!",](?:\s|$))', r"\1", comment)  # remove white space between text and interpunction
        comment = re.sub("\s*([>])\s*", r"\1", comment)  # remove space between line breaks
        comment = re.sub(" +", " ", comment)  # Remove multi-white space
        comment = re.sub(">+", ">", comment)  # Remove multi-linebreaks
        comment = comment.strip(" >")
        return comment
