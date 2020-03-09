import collections

from praw import Reddit
from praw.models.reddit.comment import Comment
from datetime import datetime
import natural.date as dt
import time
import numpy as np
import sqlite3

reddit = Reddit(client_id='OFsSWAsbFrzLpg',
                     client_secret='tRReu7VAAyxgEXbGqaE19_OUrR4',
                     password='Bohbut-xinkoq-sahca1',
                     user_agent='testscript by /u/pocaguirre',
                     username='pocaguirre')


def get_db():
    conn = sqlite3.connect('../database.db')
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
    print(comments)
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
        for word, word_cnt in texts_dict.items():
            data.append({'tag': word, 'weight': np.random.randint(100), 'color': colors[i]})
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
    print(data)
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