import os
import subprocess
import re

def print2(comment):
    print(re.sub(r'>',r'\n',comment))
    
def print2_list(comment_list):
    for x in comment_list:
        print2(x)
        print('\n-------\n')
        
        
def export_ipynb_for_github_pages(filename,front_matter_str,prefix):
    """
    Converts the .ipynb file to a .html file with all code omitted. Also replaces 
    all occurences of '{{' with '{ {' because otherwise this gives issues when Jekyll 
    parses the file.
    
    Edited from https://davistownsend.github.io/blog/PlotlyBloggingTutorial/
    """
    filename_html = prefix + re.sub('ipynb','html',filename)
    subprocess.call(["jupyter", "nbconvert","--to","html","--template","hidecode",filename,"--output",filename_html])

    subprocess.call(["sed", "-i", "s/{{/{ {/g", filename_html])
    subprocess.call(["sed", "-i", "s/.navbar/.navbar2/g", filename_html])
    subprocess.call(["sed", "-i", "s/.nav /.nav2 /g", filename_html])
    subprocess.call(["sed", "-i", "s/.container-fluid /.container-fluid2 /g", filename_html])
    
    with open(filename_html, 'r') as original: 
        data = original.read()
    with open(filename_html, 'w') as modified: 
        modified.write(front_matter_str + "\n" + data)