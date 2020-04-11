import collections

from praw import Reddit
from praw.models.reddit.comment import Comment
from datetime import datetime

import re
import time
import json
import numpy as np
import pandas as pd
import pymysql.cursors
import natural.date as dt

reddit = Reddit(client_id='OFsSWAsbFrzLpg',
                     client_secret='tRReu7VAAyxgEXbGqaE19_OUrR4',
                     password='Bohbut-xinkoq-sahca1',
                     user_agent='testscript by /u/pocaguirre',
                     username='pocaguirre')


with open("subreddit_thumbnails.json", "r") as f:
    subreddit_list = json.load(f)
    subreddit_df = pd.DataFrame(subreddit_list)


def check_user(username, password):
    c, _ = get_db()
    c.execute("select passwd = password(%s) as flag from Users where username = %s", (password, username))
    check = c.fetchall()
    if len(check) == 1:
        return bool(check[0]['flag'])
    else:
        return False

def get_user_info(username):
    c, _ = get_db()
    c.execute("select username, name from Users where username = %s", (username,))
    check = c.fetchall()
    return {'username': check[0]['username'], "name": check[0]['name']}


def get_db():
    conn = pymysql.connect(
        host="localhost",
        user="carlos",
        passwd="clsprules",
        db="LearnThisLanguageBot",
        cursorclass=pymysql.cursors.DictCursor
    )
    cur = conn.cursor()
    return cur, conn


def show_comment(comment):
    trans_obj = {'translated': {}, 'parent': {},'request': {}, 'footer': {}}

    now = datetime.fromtimestamp(time.time())

    trans_obj['translated']['body'] = comment['body']
    trans_obj['translated']['points'] = comment['points']
    trans_obj['translated']['author'] = comment['author_id']
    trans_obj['translated']['url'] = "https://www.reddit.com" + comment['url']
    trans_obj['translated']['time'] = dt.duration(comment['time'], now=now)

    trans_obj['request']['body'] = comment['request_body']
    trans_obj['request']['points'] = comment['request_points']
    trans_obj['request']['author'] = comment['request_author_id']
    trans_obj['request']['url'] = "https://www.reddit.com" + comment['request_url']
    trans_obj['request']['time'] = dt.duration(comment['request_time'], now=now)

    trans_obj['parent']['body'] = comment['sc.body']
    trans_obj['parent']['points'] = comment['sc.points']
    trans_obj['parent']['author'] = comment['sc.author_id']
    trans_obj['parent']['url'] = "https://www.reddit.com" + comment['sc.url']
    trans_obj['parent']['time'] = dt.duration(comment['sc.time'], now=now)

    trans_obj['footer']['url'] = comment['submission_url']
    trans_obj['footer']['title'] = comment['submission_title']
    trans_obj['footer']['subreddit'] = comment['submission_subreddit_id']
    trans_obj['footer']['points'] = comment['submission_points']
    trans_obj['footer']['comments'] = comment['submission_comment_cnt']

    return trans_obj

def cache_comment(sql_cur, id=None, url=None):
    if id is None and url is None:
        raise ValueError("Must provide either id or url of the comment")
    if id is not None:
        comment = reddit.comment(id=id)
    else:
        comment = reddit.comment(url=url)

    trans_obj = {'translated': {}, 'parent': {},'request': {}, 'footer': {}}
    source_comment, target_comment = {}, {}

    target_comment['comment_id'] = comment.id
    target_comment['body'] = comment.body_html
    target_comment['points'] = comment.score
    target_comment['author_id'] = comment.author.name
    target_comment['url'] = "https://www.reddit.com"+comment.permalink
    target_comment['time'] = datetime.fromtimestamp(comment.created)
    target_comment['lang_id'] = 'NA'

    target_comment['request_comment_id'] = comment.parent().id
    target_comment['request_body'] = comment.parent().body_html
    target_comment['request_points'] = comment.parent().score
    target_comment['request_author_id'] = comment.parent().author.name
    target_comment['request_url'] = comment.parent().permalink
    target_comment['request_time'] = datetime.fromtimestamp(comment.parent().created)

    parent = comment.parent().parent()
    if type(parent) == Comment:
        source_comment['comment_id'] = parent.id
        source_comment['body'] = parent.body_html
        source_comment['points'] = parent.score
        source_comment['author_id'] = parent.author.name
        source_comment['url'] = parent.permalink
        source_comment['time'] = datetime.fromtimestamp(parent.created)
    else:
        source_comment['comment_id'] = parent.flair.submission.id
        source_comment['body'] = parent.flair.submission.selftext_html
        source_comment['title'] = parent.flair.submission.title
        source_comment['points'] = parent.flair.submission.score
        source_comment['author_id'] = parent.flair.submission.author.name
        source_comment['url'] = parent.flair.submission.url
        source_comment['time'] = datetime.fromtimestamp(parent.flair.submission.created)
    source_comment['lang_id'] = 'NA'

    submission = comment.submission
    target_comment['submission_url'] = submission.url
    target_comment['submission_title'] = submission.title
    target_comment['submission_subreddit_id'] = submission.subreddit_name_prefixed
    target_comment['submission_points'] = submission.score
    target_comment['submission_comment_cnt'] = submission.num_comments
    target_comment['source_comment_id'] = source_comment['comment_id']

    placeholders = ', '.join(['%s'] * len(source_comment))
    columns = ', '.join(source_comment.keys())
    sql_cur.execute('INSERT IGNORE INTO SourceComment (%s) VALUES (%s)' % (columns, placeholders), tuple(source_comment.values()))

    placeholders = ', '.join(['%s'] * len(target_comment))
    columns = ', '.join(target_comment.keys())
    sql_cur.execute('INSERT IGNORE INTO TargetComment (%s) VALUES (%s)' % (columns, placeholders), tuple(target_comment.values()))

    return source_comment, target_comment


def get_all_comments():
    sql_cur, _ = get_db()
    sql_cur.execute("SELECT * FROM TargetComment AS tc LEFT JOIN SourceComment AS sc ON (tc.source_comment_id = sc.comment_id)")
    comments = []
    for row in sql_cur:
        comments.append(show_comment(row))
    return comments


def get_user_comments(user):
    sql_cur, _ = get_db()
    sql_cur.execute(
        "SELECT * FROM TargetComment AS tc LEFT JOIN SourceComment AS sc ON (tc.source_comment_id = sc.comment_id) WHERE tc.request_author_id = %s",
        (user,))
    comments = []
    for row in sql_cur:
        comments.append(show_comment(row))
    return comments


def get_table(user):
    sql_cur, _ = get_db()
    sql_cur.execute(
        "SELECT subreddit_id, rec_score FROM UserRecommendedSubreddits WHERE user_id = %s ORDER BY rec_score DESC LIMIT 10",
        (user,))
    data = []
    for row in sql_cur:
        data.append((row['subreddit_id'], row['rec_score']))
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
    cleanr = re.compile('<.*?>')
    sql_cur, _ = get_db()
    data = []
    colors = ['#FCBA03', '#0388FC', '#FC032D']
    sql_cur.execute(
        "SELECT lang_id, body FROM TargetComment WHERE request_author_id = %s", (user,))
    texts = collections.defaultdict(collections.Counter)
    for row in sql_cur:
        text = row['body'].strip()
        text = re.sub(cleanr, '', text)
        text = text.split()
        texts[row['lang_id']].update(text)
    languages = []
    for i, (lang_id, texts_dict) in enumerate(texts.items()):
        languages.append(lang_id)
        for j, (word, word_cnt) in enumerate(texts_dict.items()):
            if j > 25:
                break
            data.append({'tag': word, 'weight': np.random.randint(50, 100), 'color': colors[i]})
    print(user)
    return {"data": data, 'legend': [{"name": lan, "fill": c} for lan, c in zip(languages, colors)]}


def get_bar_chart(user):
    cleanr = re.compile('<.*?>')
    sql_cur, _ = get_db()
    colors = ['#FCBA03', '#0388FC', '#FC032D']
    sql_cur.execute(
        "SELECT lang_id, body, submission_subreddit_id FROM TargetComment WHERE request_author_id = %s", (user,))
    languages = set()
    texts = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
    for row in sql_cur:
        text = row['body'].strip()
        text = re.sub(cleanr, '', text)
        text = text.split()
        texts[row['submission_subreddit_id']][row['lang_id']].update(text)
        languages.add(row['lang_id'])
    data = []
    for subreddit_id, text in texts.items():
        data_item = {'subreddit': subreddit_id}
        for lang_id, counter in text.items():
            data_item[lang_id] = sum(counter.values())
        data.append(data_item)

    return {"data": data, 'languages': list(languages), 'colors': colors}


def get_flash_cards(user):
    sql_cur, _ = get_db()
    data = []
    colors = ['#FCBA03', '#0388FC', '#FC032D']
    sql_cur.execute(
        "SELECT src_lang_word, tgt_lang_word, tgt_lang_id FROM UserLearnProgress WHERE user_id = %s", (user,))
    words = collections.defaultdict(list)
    for row in sql_cur:
        words[row['tgt_lang_id']].append((row['src_lang_word'], row['tgt_lang_word']))

    cards = [
        {'language': language, 'color': color,
         "words": [{"front": tgt, "back": src} for src, tgt in pairs]} for (language, pairs), color in zip(words.items(), colors)
    ]
    return cards


def get_recommendations(user):
    sql_cur, _ = get_db()
    sql_cur.execute(
        "SELECT subreddit_id, rec_score FROM UserRecommendedSubreddits WHERE user_id = %s ORDER BY rec_score DESC LIMIT 10",
        (user,))
    data = []
    for row in sql_cur:
        subred = subreddit_df[subreddit_df['subreddit'].str.lower() == row['subreddit_id'].lower()]
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
        data.append({"name": row['subreddit_id'], "score": row['rec_score'], "href": href})
    columns = ["subreddit", "rec_score"]
    return columns, data
