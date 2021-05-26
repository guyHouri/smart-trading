#############################################################################
#
# smart trading project - guy houri
#
# Purpose: To analyze the sentiments of the reddit
# This program uses Vader SentimentIntensityAnalyzer to calculate the ticker compound value. 
#
#############################################################################

import praw # PRAW, an acronym for “Python Reddit API Wrapper”, is a Python package that allows for simple access for reddit api
import sys
sys.path.append(r"D:\yudgimel\project\stocks")
from redditData import *
import time
import pandas as pd
import squarify #
from nltk.sentiment.vader import SentimentIntensityAnalyzer # Natural Language Toolkit

start_time = time.time()

import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"]  = [16,9] # size of graph
plt.rcParams["lines.linewidth"] = 0.75   # lines width
plt.rcParams.update({'font.size': 22})   # font size


# set up and connect reddit api
reddit = praw.Reddit(
    user_agent="Comment Extraction",
    client_id="oh8OoK_GVWtrxA",
    client_secret="7ak5eGyYS9xGf_bzlAgMVJiWxyt-kg"
)


# set the program parameters
subs = ['wallstreetbets', 'stocks', 'investing', 'stockmarket'] # sub-reddit to search
post_flairs = {'Daily Discussion', 'Weekend Discussion', 'Discussion'} # posts flairs ('categorizing' posts submitted by users) to search || None flair is automatically considered
goodAuth = {'AutoModerator'} # מנהלים
uniqueCmt = True # allow one comment per author per symbol
ignoreAuthP = {'example'} # authors to ignore for posts 
ignoreAuthC = {'example'} # authors to ignore for comment 
upvoteRatio = 0.70 # upvote ratio for post to be considered, 0.70 = 70%
ups = 20 # define # of upvotes, post is considered if upvotes exceed this #
limit = 10 # define the limit, comments 'replace more' limit
upvotes = 2 # define # of upvotes, comment is considered if upvotes exceed this #
picks = 10 # define # of picks here, prints as "Top ## picks are:"
picks_ayz = 5 # define # of picks for sentiment analysis. takes a lot of time so i did only 5

posts, count, c_analyzed, tickers, titles, a_comments = 0, 0, 0, {}, [], {}
cmt_auth = {}

# main loop
for sub in subs: # for each subreddit (foroum)
    subreddit = reddit.subreddit(sub)
    hot_python = subreddit.hot()    # sorting posts by hot - get 25 most popular posts

    # Extracting comments, symbols from subreddit
    for submission in hot_python: # for each post
        flair = submission.link_flair_text 
        if submission.author is not None:
            author = submission.author.name
        else:
            author = ""         
        
        # checking: post upvote ratio # of upvotes, post flair, and author 
        if submission.upvote_ratio >= upvoteRatio and submission.ups > ups and (flair in post_flairs or flair is None) and author not in ignoreAuthP:   
            submission.comment_sort = 'new'     
            comments = submission.comments
            titles.append(submission.title)
            posts += 1
            submission.comments.replace_more(limit=limit)   

            for comment in comments:
                # try except for deleted account?
                try: auth = comment.author.name
                except: pass
                c_analyzed += 1
                
                # checking: comment upvotes and author
                if comment.score > upvotes and auth not in ignoreAuthC:      
                    split = comment.body.split(" ") # array of all the words in the comment

                    for word in split:
                        word = word.replace("$", "")   

                        # upper = ticker, length of ticker <= 5, excluded words. we check if the word is a ticker                     
                        if word.isupper() and len(word) <= 5 and word not in blacklist and word in alltickers:
                            
                            # unique comments, try/except for key errors
                            if uniqueCmt and auth not in goodAuth:
                                try: 
                                    if auth in cmt_auth[word]: break
                                except: pass
                                
                            # counting tickers
                            if word in tickers:
                                tickers[word] += 1
                                a_comments[word].append(comment.body) # for sentiment analysise add body of comment to dictionary
                                cmt_auth[word].append(auth)
                                count += 1
                            else: #fisrt time we saw stocks                              
                                tickers[word] = 1
                                cmt_auth[word] = [auth]
                                a_comments[word] = [comment.body]
                                count += 1    

# sorts the dictionary
symbols = dict(sorted(tickers.items(), key=lambda item: item[1], reverse = True)) # at the top will be the most seen ticker
top_picks = list(symbols.keys())[0:picks] # extract array of the tickers
time = (time.time() - start_time)

# print top picks
from myDate import*
dt_now = dt_string
print("It took {t:.2f} seconds to analyze {c} comments in {p} posts in {s} subreddits. {dt}\n".format(t=time, c=c_analyzed, p=posts, s=len(subs), dt=dt_now))
print("Posts analyzed saved in titles")
#for i in titles: print(i)  # prints the title of the posts analyzed

print(f"\n{picks} most mentioned picks: ")
times = []
top = []
for i in top_picks:
    print(f"{i}: {symbols[i]}")
    times.append(symbols[i])
    top.append(f"{i}: {symbols[i]}")
   
    
# Applying Sentiment Analysis
scores, s = {}, {}
 
vader = SentimentIntensityAnalyzer()
# adding custom words from data.py 
vader.lexicon.update(new_words)

picks_sentiment = list(symbols.keys())[0:picks_ayz] # first 5
for symbol in picks_sentiment:
    stock_comments = a_comments[symbol]
    for cmnt in stock_comments:
        score = vader.polarity_scores(cmnt)
        if symbol in s:
            s[symbol][cmnt] = score
        else:
            s[symbol] = {cmnt:score}      
        if symbol in scores:
            for key, _ in score.items():
                scores[symbol][key] += score[key]
        else:
            scores[symbol] = score
            
    # calculating avg.
    for key in score:
        scores[symbol][key] = scores[symbol][key] / symbols[symbol]
        scores[symbol][key]  = "{pol:.3f}".format(pol=scores[symbol][key])
 
print('\n before save image \n')
# printing sentiment analysis 
print(f"\nSentiment analysis of top {picks_ayz} picks:")
df = pd.DataFrame(scores)
df.index = ['negative', 'Neutral', 'positive', 'Total/Compound']
df = df.T
print(df)

# Date Visualization
# most mentioned picks    


squarify.plot(sizes=times, label=top, alpha=.7 )
plt.axis('off')
plt.title(f"{picks} most mentioned picks")
mentioned_picks_fig_place = r"D:/yudgimel/project/website/static/images/redditSen/"+'10mentioned.PNG'
title_obj = plt.title('reddit top 5 talked about figs') #get the title property handler
plt.setp(title_obj, color='r')         #set the color of title to red
plt.savefig(mentioned_picks_fig_place, facecolor="white", edgecolor="none")

# Sentiment analysis
df = df.astype(float)
colors = ['red', 'springgreen', 'forestgreen', 'coral']
df.plot(kind = 'bar', color=colors, title=f"reddit top {picks_ayz} talked about stocks of today:", edgecolor='gold')
sentiment_anylasise_fig_place = r"D:/yudgimel/project/website/static/images/redditSen/"+'5analyasise.PNG'
title_obj = plt.title('reddit top 5 talked about figs') #get the title property handler
plt.setp(title_obj, color='r')         #set the color of title to red
plt.savefig(sentiment_anylasise_fig_place, facecolor="white", edgecolor="none")


print("saved")

