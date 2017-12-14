# creates a subreddit-subreddit network from a given user-subreddit network

import sys
import shlex, subprocess
import time

startTime = time.time()

user_sub_file = sys.argv[1]
sub_sub_file = sys.argv[1].split('.')[0]+".subreddit_subreddit.csv"

bunchsize = 1000000
bunch = 0
count = 0

print("### making projection")

currUser = ""
currSubs = {}

sub_sub = {}

with open(user_sub_file, "r") as r:
    for line in r:
        (user, subreddit) = line.split(',')
        subreddit = subreddit.split('\n')[0]
        if not currUser == user:
            # new user: make edges for currSubs. ignore currUser == "" since we're in line 1
            if not currUser == "":
                for sub1, sub1v in currSubs.items():
                    for sub2, sub2v in currSubs.items():
                        if sub1 == sub2: 
                            # no self loops
                            continue
                        if sub1 > sub2:
                            # swap places so we only have edges from lower subreddit to higher subreddit, lexicographically
                            sub_temp = sub1
                            subv_temp = sub1v
                            sub1 = sub2
                            sub1v = sub2v
                            sub2 = sub_temp
                            sub2v = subv_temp
                        if not sub1 in sub_sub:
                            sub_sub[sub1] = {}
                        # create edge
                        if not sub2 in sub_sub[sub1]:
                            sub_sub[sub1][sub2] = 0
                        weight = sub1v * sub2v
                        sub_sub[sub1][sub2] += weight
            
            # clean up and prepare for new user
            currUser = user
            currSubs = {}
        
        if not subreddit in currSubs:
            currSubs[subreddit] = 0
        currSubs[subreddit] += 1
        
        bunch += 1
        if bunch == bunchsize:
            bunch = 0
            count = count + bunchsize
            print(count) 
    r.close()

print("### writing projection to disk")

with open(sub_sub_file, "w") as w:
    w.write("subredditA,subredditB,weight\n")
    for sub1,subs in sub_sub.items():
        for sub2,weight in subs.items():
            w.write(sub1+","+sub2+","+str(weight)+"\n")
    w.close()

startTime = time.time() - startTime
print("### done!")
print("### wrote file "+sub_sub_file)
print("### elapsed time:", startTime, "sec")