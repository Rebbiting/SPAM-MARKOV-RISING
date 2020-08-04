import praw
from praw.models import MoreComments
import time
import numpy as np
import random
import traceback

CLIENT_ID = "CLIENT_ID"
CLIENT_SECRET = "CLIENT_SECRET"
USER_AGENT = "Type random shit here."
USERNAME = "USERNAME"
PASSWORD = "PASSWORD"
FILE_NAME = "FILE NAME"
MIN_WORD_COUNT = "Mininum words for the comment"
MAX_WORD_COUNT = "Softlimit for the word count. Will continue until the string ends with one of the END_STRINGS"
END_STRINGS = ('.', '!', '?') # The comment will always end with these (make sure they are in the text file). It is a tuple.

print("Starting")

while True:
    try:
        def make_pairs(words):
            for i in range(len(words)-1):
                yield words[i], words[i + 1]

        def markov(troll,c_min,c_max,endw):
            text = open('{}.txt'.format(troll), encoding='utf8').read()
            words = text.split()
            pairs = make_pairs(words)
            word_dict = {}
            for word_1, word_2 in pairs:
                if word_1 in word_dict.keys():
                    word_dict[word_1].append(word_2)
                else:
                    word_dict[word_1] = [word_2]

            first_word = np.random.choice(words)
            while first_word.islower():
                first_word = np.random.choice(words)
            chain = [first_word]
            word_c = random.randint(c_min,c_max)
            try:
                try:
                    for i in range(word_c):
                        ran_word = np.random.choice(word_dict[chain[-1]])
                        chain.append(ran_word)
                except:
                    for i in range(0):
                        ran_word = np.random.choice(word_dict[chain[-1]])
                        chain.append(ran_word)
            except:
                traceback.print_exc()
            while ' '.join(chain).endswith(endw) == False:
                chain.append(np.random.choice(word_dict[chain[-1]]))
            return ' '.join(chain)

        print("Logging on.")
        reddit = praw.Reddit(client_id = CLIENT_ID,
                             client_secret = CLIENT_SECRET,
                             user_agent = USER_AGENT,
                             username = USERNAME,
                             password = PASSWORD)
        
        print("Logged on.")
        j = 0
        while True:
                for submission in reddit.subreddit('All').rising(limit=25):
                    try:
                        submission.comment_sort='confidence'
                        submission.comment_limit=3
                        for comment in submission.comments:
                            try:
                                if isinstance(comment,MoreComments):
                                    continue
                                if not comment.distinguished and not submission.saved:
                                    my_comment = comment.reply(markov(FILE_NAME, MIN_WORD_COUNT, MAX_WORD_COUNT, END_STRINGS))
                                    print(my_comment)
                                    submission.save()
                                    j = 0
                                    time.sleep(10)
                                    break
                            except Exception as e:
                                if j >= 4:
                                    submission.save()
                                j = j + 1
                                print(repr(e))
                                time.sleep(10)
                    except Exception as e:
                        print(repr(e))
                        time.sleep(10)
    except:
        traceback.print_exc()
        time.sleep(10)
