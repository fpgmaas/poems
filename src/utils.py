import os
import subprocess
import re


def print2(comment):
    print(re.sub(r">", r"\n", comment))


def print2_list(comment_list):
    for x in comment_list:
        print2(x)
        print("\n-------\n")
