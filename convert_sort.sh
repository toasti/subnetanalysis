#!/bin/sh

head -n 1 data/user_subreddit.csv > data/user_subreddit.csv_temp && tail -n +2 data/user_subreddit.csv | sort -t "," -k 1 >> data/user_subreddit.csv_temp

mv data/user_subreddit.csv_temp data/user_subreddit.csv
