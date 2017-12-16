# reads a .subreddit-subreddit.csv file and collects information about all subreddits in .substats.csv

# todo: status updates https://stackoverflow.com/questions/517127/how-do-i-write-output-in-same-place-on-the-console

import sys
import shlex, subprocess
import time
import json
import praw
import prawcore

startTime = time.time()

sub_sub_file = sys.argv[1]
substats_file = sys.argv[1].split('.')[0]+".substats.csv"

print("### getting list of unique subreddit names in file")

subreddits = set()

with open(sub_sub_file, "r", newline='') as r:
    skipheader = True
    for line in r:
        if skipheader:
            skipheader = False
            continue
        (subreddit1, subreddit2, weight) = line.split(',')
        subreddits.add(subreddit1)
        subreddits.add(subreddit2)
    r.close()

print("### scraping and writing data")

with open(substats_file, "w") as w:
    w.write("subreddit,over18,subcount\n")
    reddit = praw.Reddit(client_id='ptqut-k8w4nKUA',
                     client_secret='sYhFCA0o3Otj5c85BEIyxD48JXE',
                     user_agent='subnetanalysis:v0.1 by /u/t0asti')
    
    count = 0
    sys.stdout.write(" "+str(count)+"/"+str(len(subreddits))+"\r")
    sys.stdout.flush()
    
    for currSub in subreddits:
        try:
            r_currSub = reddit.subreddit(currSub)
            w.write(currSub + ","+ str(r_currSub.over18) + "," + str(r_currSub.subscribers)+"\n")
        except prawcore.exceptions.NotFound:
            print("banned sub:", currSub)
            w.write(currSub + ",null,null"+"\n")
        except prawcore.exceptions.Forbidden:
            print("private sub:", currSub)
            w.write(currSub + ",null,null"+"\n")
        except AssertionError:
            print("banned sub?", currSub)
            w.write(currSub + ",null,null"+"\n")
       
        count += 1
        if count % 10 == 0:
           sys.stdout.write(" "+str(count)+"/"+str(len(subreddits))+"\r")
           sys.stdout.flush()
        
    w.close()

startTime = time.time() - startTime
print("### done!")
print("### wrote file "+substats_file)
print("### elapsed time:", startTime, "sec")