# reads the reddit comment data dump line by line and creates a new adjacency list for user->subreddit, writes it and orders it by user

import json
from subprocess import call

dump_file = "data/sample_data.json"
adj_file = "data/user_subreddit.csv"


bunchsize = 1000000    # write less often
bunch = []
count = 0

print("### writing adjacency list")

with open(dump_file, "r") as r, open(adj_file, "w") as w:
    w.write("user,subreddit\n")
    for line in r:
        json_obj = json.loads(line)
        author = json_obj['author']
        subreddit = json_obj['subreddit']
        if author == "AutoModerator":   # skip automod
            continue
        bunch.append(author + "," + subreddit + "\n")
        if len(bunch) == bunchsize:
            w.writelines(bunch)
            bunch= []
            count = count + bunchsize
            print(count)
    w.writelines(bunch)
    w.close()
    r.close()

print("### sorting...")

call('./convert_sort.sh')      # use unix sort because it's faster than doing it in python

print("### done!")

# finished