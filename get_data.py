
#####################
### Imports
#####################

import collections

from praw import Reddit
from praw.models.reddit.comment import Comment
from datetime import datetime
import natural.date as dt
import time
import numpy as np
import sqlite3
import json
import pandas as pd

## Recommendation
from rrec.acquire.reddit import RedditData
from rrec.model.reddit_recommender import RedditRecommender

#####################
### Globals
#####################

reddit = Reddit(client_id='OFsSWAsbFrzLpg',
                     client_secret='tRReu7VAAyxgEXbGqaE19_OUrR4',
                     password='Bohbut-xinkoq-sahca1',
                     user_agent='testscript by /u/pocaguirre',
                     username='pocaguirre')

## Initialize PSAW (Fast Reddit Data Queries)
psaw = RedditData()

## Initialize Recommendation Model
REC_MODEL_PATH = "./rrec/models/comments_20200221_20200228.cf"
recommender = RedditRecommender(REC_MODEL_PATH)

## Recommendation Database Paths
DB_PATH = "./rrec/data/db/"
USER_HISTORY_DB_PATH = f"{DB_PATH}user_history.db"
RECOMMENDATION_HISTORY_DB_PATH = f"{DB_PATH}recommendations.db"

## Subreddit Thumbnails
with open("subreddit_thumbnails.json", "r") as f:
    subreddit_list = json.load(f)
    subreddit_df = pd.DataFrame(subreddit_list)

#####################
### Functions
#####################

def check_user(username, password):
    c = get_db()
    data = (username, password)
    c.execute("select username, passwd from users where username = ?", [username])
    check = c.fetchall()
    if check == []:
        return False
    else:
        check = check[0]
        if data == check:
            return True
        else:
            return False

def get_user_info(username):
    c = get_db()
    c.execute("select username, name from users where username = ?", [username])
    check = c.fetchall()
    return {'username': check[0][0], "name": check[0][1]}


def get_db():
    conn = sqlite3.connect('./database.db')
    cur = conn.cursor()
    return cur


def get_comment(id=None, url=None):
    if id is None and url is None:
        raise ValueError("Must provide either id or url of the comment")
    if id is not None:
        comment = reddit.comment(id=id)
    else:
        comment = reddit.comment(url=url)
    trans_obj = {'translated': {}, 'parent': {},'request': {}, 'footer': {}}

    trans_obj['translated']['body'] = comment.body_html
    trans_obj['translated']['points'] = comment.score
    trans_obj['translated']['author'] = comment.author.name
    trans_obj['translated']['url'] = "https://www.reddit.com"+comment.permalink
    trans_obj['translated']['time'] = dt.duration(datetime.fromtimestamp(comment.created),
                                                  now=datetime.fromtimestamp(time.time()))

    trans_obj['request']['body'] = comment.parent().body_html
    trans_obj['request']['points'] = comment.parent().score
    trans_obj['request']['author'] = comment.parent().author.name
    trans_obj['request']['url'] = "https://www.reddit.com" + comment.parent().permalink
    trans_obj['request']['time'] = dt.duration(datetime.fromtimestamp(comment.parent().created),
                                                  now=datetime.fromtimestamp(time.time()))
    parent = comment.parent().parent()
    if type(parent) == Comment:
        trans_obj['parent']['body'] = parent.body_html
        trans_obj['parent']['points'] = parent.score
        trans_obj['parent']['author'] = parent.author.name
        trans_obj['parent']['url'] = "https://www.reddit.com" + parent.permalink
        trans_obj['parent']['time'] = dt.duration(datetime.fromtimestamp(parent.created),
                                                   now=datetime.fromtimestamp(time.time()))
    else:
        trans_obj['parent']['body'] = parent.flair.submission.selftext_html
        trans_obj['parent']['title'] = parent.flair.submission.title
        trans_obj['parent']['points'] = parent.flair.submission.score
        trans_obj['parent']['author'] = parent.flair.submission.author.name
        trans_obj['parent']['url'] = parent.flair.submission.url
        trans_obj['parent']['time'] = dt.duration(datetime.fromtimestamp(parent.flair.submission.created),
                                                  now=datetime.fromtimestamp(time.time()))
    submission = comment.submission
    trans_obj['footer']['url'] = submission.url
    trans_obj['footer']['title'] = submission.title
    trans_obj['footer']['subreddit'] = submission.subreddit_name_prefixed
    trans_obj['footer']['points'] = submission.score
    trans_obj['footer']['comments'] = submission.num_comments
    return trans_obj


def get_all_comments():
    sqlite_cur = get_db()
    rows = sqlite_cur.execute("SELECT bot_comment_id FROM TranslatedComments")
    comments = []
    for url, in rows:
        comments.append(get_comment(url=url))
    return comments


def get_user_comments(user):
    sqlite_cur = get_db()
    rows = sqlite_cur.execute(
        "SELECT bot_comment_id FROM TranslatedComments WHERE requester_user_id = ?",
        (user,))
    comments = []
    for url, in rows:
        comments.append(get_comment(url=url))
    return comments


def get_table(user):
    sqlite_cur = get_db()
    rows = sqlite_cur.execute(
        "SELECT subreddit_id, rec_score FROM UserRecommendedSubreddits WHERE user_id = ? ORDER BY rec_score DESC LIMIT 10",
        (user,))
    data = []
    for row in rows:
        data.append(row)
    columns = ["subreddit", "rec_score"]
    return columns, data


def get_stack_bar(user):
    data = [{
        "week": "11/04/19",
        "es": 1587,
        "fr": 650,
    }, {
        "week": "11/11/19",
        "es": 1567,
        "fr": 683,
    }, {
        "week": "11/18/19",
        "es": 1617,
        "fr": 691,
    }, {
        "week": "11/25/19",
        "es": 1630,
        "fr": 642,
    }, {
        "week": "12/2/19",
        "es": 1660,
        "fr": 699,
    }, {
        "week": "12/9/19",
        "es": 1683,
        "fr": 721,
    }, {
        "week": "12/16/19",
        "es": 1691,
        "fr": 737,
    }, {
        "week": "12/23/19",
        "es": 1298,
        "fr": 680,
    }, {
        "week": "12/30/19",
        "es": 1275,
        "fr": 664,
    }, {
        "week": "01/06/20",
        "es": 1246,
        "fr": 648,
    }, {
        "week": "01/13/20",
        "es": 1318,
        "fr": 697,
    }, {
        "week": "01/20/20",
        "es": 1213,
        "fr": 633,
    }, {
        "week": "01/27/20",
        "es": 1199,
        "fr": 621,
    }, {
        "week": "02/03/20",
        "es": 1110,
        "fr": 210,
    }, {
        "week": "02/10/20",
        "es": 1165,
        "fr": 232,
    }, {
        "week": "02/17/20",
        "es": 1145,
        "fr": 219,
    }, {
        "week": "02/24/20",
        "es": 1163,
        "fr": 201,
    }, {
        "week": "03/02/20",
        "es": 1180,
        "fr": 285,
    }, {
        "week": "03/09/20",
        "es": 1159,
        "fr": 277,
    }]
    return {'data': data, 'languages': ['es', 'fr'], 'colors': ['#FCBA03', '#0388FC']}


def get_word_cloud(user):
    sqlite_cur = get_db()
    data = []
    colors = ['#FCBA03', '#0388FC', '#FC032D']
    rows = sqlite_cur.execute(
        "SELECT tgt_lang_id, tgt_text FROM TranslatedComments WHERE requester_user_id = ?", (user,))
    texts = collections.defaultdict(collections.Counter)
    for (lang_id, tgt_text_str) in rows:
        text = tgt_text_str.strip().split()
        texts[lang_id].update(text)
    languages = []
    for i, (lang_id, texts_dict) in enumerate(texts.items()):
        languages.append(lang_id)
        for j, (word, word_cnt) in enumerate(texts_dict.items()):
            if j > 25:
                break
            data.append({'tag': word, 'weight': np.random.randint(50, 100), 'color': colors[i]})
    return {"data": data, 'legend': [{"name": lan, "fill": c} for lan, c in zip(languages, colors)]}


def get_bar_chart(user):
    sqlite_cur = get_db()
    colors = ['#FCBA03', '#0388FC', '#FC032D']
    rows = sqlite_cur.execute(
        "SELECT tgt_lang_id, tgt_text, subreddit_id FROM TranslatedComments WHERE requester_user_id = ?", (user,))
    languages = set()
    texts = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
    for (lang_id, tgt_text_str, subreddit_id) in rows:
        text = tgt_text_str.strip().split()
        texts[subreddit_id][lang_id].update(text)
        languages.add(lang_id)
    data = []
    for subreddit_id, text in texts.items():
        data_item = {'subreddit': 'r/' + subreddit_id}
        for lang_id, counter in text.items():
            data_item[lang_id] = sum(counter.values())
        data.append(data_item)
    return {"data": data, 'languages': list(languages), 'colors': colors}


def get_flash_cards(user):
    sqlite_cur = get_db()
    data = []
    colors = ['#FCBA03', '#0388FC', '#FC032D']
    rows = sqlite_cur.execute(
        "SELECT src_lang_word, tgt_lang_word, tgt_lang_id FROM UserLearnProgress WHERE user_id = ?", (user,))
    words = collections.defaultdict(list)
    for (src_word, tgt_word, tgt_lang) in rows:
        words[tgt_lang].append((src_word, tgt_word))

    cards = [
        {'language': language, 'color': color,
         "words": [{"front": tgt, "back": src} for src, tgt in pairs]} for (language, pairs), color in zip(words.items(), colors)
    ]
    return cards

def initialize_user_recommendations(user):
    """

    """
    ## Dates
    GLOBAL_START_DATE = "2018-01-01"
    TODAY = datetime.now().date().isoformat()
    ## Query User Comment Data
    user_comments = psaw.retrieve_author_comments(user, start_date=GLOBAL_START_DATE, end_date=TODAY)
    ## Make Recommendations
    subreddit_counts = user_comments["subreddit"].value_counts().to_dict()
    recommendations = recommender.recommend(subreddit_counts, k_top=100, filter_liked=True)
    ## Format User History for Database
    subreddit_counts = user_comments.groupby(["author"])["subreddit"].value_counts().rename("COMMENT_COUNT").reset_index()
    subreddit_counts["QUERY_START_DATE"] = GLOBAL_START_DATE
    subreddit_counts["QUERY_END_DATE"] = TODAY
    subreddit_counts.rename(columns={"author":"USER","subreddit":"SUBREDDIT"},inplace=True)
    ## Update User History Table
    user_history_con = sqlite3.connect(USER_HISTORY_DB_PATH)
    subreddit_counts.to_sql("HISTORY", user_history_con, if_exists="append", index=False)
    user_history_con.commit()
    user_history_con.close()
    ## Identify Most Popular Subreddits (Default Recommendations)
    full_comment_distribution = pd.Series(index=recommender.cf._items,
                                          data=np.array(recommender.cf._item_user_matrix.sum(axis=1)).T[0])
    top_subreddits = full_comment_distribution.nlargest(100)
    top_subreddits = top_subreddits / top_subreddits.max()
    top_subreddits = pd.DataFrame(top_subreddits).rename(columns={0:"Recommendation Score"})
    top_subreddits.index.name="item"
    ## No-valid Recommendations (e.g. no user history matches)
    if recommendations.values.max() == 0:
        recommendations = top_subreddits.copy()
    ## Format
    recommendations = recommendations.reset_index().rename(columns={"item":"SUBREDDIT","Recommendation Score":"SCORE"})
    recommendations["USER"] = user
    recommendations["REC_DATE"] = TODAY
    ## Upload Recommendations
    rec_con = sqlite3.connect(RECOMMENDATION_HISTORY_DB_PATH)
    recommendations.to_sql("RECOMMENDATIONS", con=rec_con, if_exists="append",index=False)
    rec_con.commit()
    rec_con.close()
    

def get_recommendations(user):
    rec_con = sqlite3.connect(RECOMMENDATION_HISTORY_DB_PATH)
    cursor = rec_con.cursor()
    ## Get Max Recommendation Date
    max_date = cursor.execute("SELECT MAX(REC_DATE) FROM RECOMMENDATIONS WHERE USER = ?", (user, ))
    max_date = max_date.fetchall()[0][0]
    ## Get Recommendations
    rows = cursor.execute(
        "SELECT SUBREDDIT, SCORE FROM RECOMMENDATIONS WHERE USER = ? AND REC_DATE = ? ORDER BY SCORE DESC LIMIT 10", (user, max_date)
    )
    ## Parse Recommendations
    data = []
    for row in rows:
        subred = subreddit_df[subreddit_df['subreddit'].str.lower() == row[0].lower()]
        if len(subred) > 0:
            if subred.iloc[0]['icon_img'] is None:
                if subred.iloc[0]['community_icon'] is not None:
                    href = subred.iloc[0]['community_icon']
                else:
                    href = "https://external-preview.redd.it/QJRqGgkUjhGSdu3vfpckrvg1UKzZOqX2BbglcLhjS70.png?auto=webp&s=c681ae9c9b5021d81b6c4e3a2830f09eff2368b5"
            else:
                href = subred.iloc[0]['icon_img']
        else:
            href = "https://external-preview.redd.it/QJRqGgkUjhGSdu3vfpckrvg1UKzZOqX2BbglcLhjS70.png?auto=webp&s=c681ae9c9b5021d81b6c4e3a2830f09eff2368b5"
        data.append({"name": row[0], "score": row[1], "href": href})
    columns = ["subreddit", "rec_score"]
    return columns, data
