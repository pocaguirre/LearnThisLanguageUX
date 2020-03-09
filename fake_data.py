from praw import Reddit
from praw.models.reddit.comment import Comment
from datetime import datetime
import natural.date as dt
import time
from random import randint
import numpy as np

reddit = Reddit(client_id='OFsSWAsbFrzLpg',
                     client_secret='tRReu7VAAyxgEXbGqaE19_OUrR4',
                     password='Bohbut-xinkoq-sahca1',
                     user_agent='testscript by /u/pocaguirre',
                     username='pocaguirre')


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


def get_table():
    data = [
        ["Tiger Nixon", "System Architect", "Edinburgh", 61, (2011, 4, 25), 320800],
        ["Tiger Nixon", "System Architect", "Edinburgh", 61, (2011, 4, 25), 320800],
        ["Tiger Nixon", "System Architect", "Edinburgh", 61, (2011, 4, 25), 320800],
        ["Tiger Nixon", "System Architect", "Edinburgh", 61, (2011, 4, 25), 320800],
        ["Tiger Nixon", "System Architect", "Edinburgh", 61, (2011, 4, 25), 320800],
        ["Tiger Nixon", "System Architect", "Edinburgh", 61, (2011, 4, 25), 320800],
        ["Tiger Nixon", "System Architect", "Edinburgh", 61, (2011, 4, 25), 320800],
        ["Tiger Nixon", "System Architect", "Edinburgh", 61, (2011, 4, 25), 320800],
        ["Tiger Nixon", "System Architect", "Edinburgh", 61, (2011, 4, 25), 320800],
        ["Tiger Nixon", "System Architect", "Edinburgh", 61, (2011, 4, 25), 320800],
        ["Tiger Nixon", "System Architect", "Edinburgh", 61, (2011, 4, 25), 320800],
        ["Tiger Nixon", "System Architect", "Edinburgh", 61, (2011, 4, 25), 320800],
        ["Tiger Nixon", "System Architect", "Edinburgh", 61, (2011, 4, 25), 320800],
        ["Tiger Nixon", "System Architect", "Edinburgh", 61, (2011, 4, 25), 320800],
        ["Tiger Nixon", "System Architect", "Edinburgh", 61, (2011, 4, 25), 320800],
        ["Tiger Nixon", "System Architect", "Edinburgh", 61, (2011, 4, 25), 320800]]
    columns = ["Name", "Position", "Office", "Age", "Start date", "Salary"]
    return columns, data


def get_stack_bar(user):
    data = [{
        "week": "11/04/19",
        "spanish": 1587,
        "french": 650,
        "russian": 121
    }, {
        "week": "11/11/19",
        "spanish": 1567,
        "french": 683,
        "russian": 146
    }, {
        "week": "11/18/19",
        "spanish": 1617,
        "french": 691,
        "russian": 138
    }, {
        "week": "11/25/19",
        "spanish": 1630,
        "french": 642,
        "russian": 127
    }, {
        "week": "12/2/19",
        "spanish": 1660,
        "french": 699,
        "russian": 105
    }, {
        "week": "12/9/19",
        "spanish": 1683,
        "french": 721,
        "russian": 109
    }, {
        "week": "12/16/19",
        "spanish": 1691,
        "french": 737,
        "russian": 112
    }, {
        "week": "12/23/19",
        "spanish": 1298,
        "french": 680,
        "russian": 101
    }, {
        "week": "12/30/19",
        "spanish": 1275,
        "french": 664,
        "russian": 97
    }, {
        "week": "01/06/20",
        "spanish": 1246,
        "french": 648,
        "russian": 93
    }, {
        "week": "01/13/20",
        "spanish": 1318,
        "french": 697,
        "russian": 111
    }, {
        "week": "01/20/20",
        "spanish": 1213,
        "french": 633,
        "russian": 87
    }, {
        "week": "01/27/20",
        "spanish": 1199,
        "french": 621,
        "russian": 79
    }, {
        "week": "02/03/20",
        "spanish": 1110,
        "french": 210,
        "russian": 81
    }, {
        "week": "02/10/20",
        "spanish": 1165,
        "french": 232,
        "russian": 75
    }, {
        "week": "02/17/20",
        "spanish": 1145,
        "french": 219,
        "russian": 88
    }, {
        "week": "02/24/20",
        "spanish": 1163,
        "french": 201,
        "russian": 82
    }, {
        "week": "03/02/20",
        "spanish": 1180,
        "french": 285,
        "russian": 87
    }, {
        "week": "03/09/20",
        "spanish": 1159,
        "french": 277,
        "russian": 71
    }]
    return {'data': data, 'languages': ['spanish', 'french', 'russian'], 'colors': ['#FCBA03', '#0388FC', '#FC032D']}


def get_word_cloud(user):

    text = "Lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et dolore magna aliqua Amet tellus cras adipiscing enim eu Purus gravida quis blandit turpis cursus In dictum non consectetur a erat nam at lectus urna Sollicitudin ac orci phasellus egestas tellus rutrum Eros donec ac odio tempor orci dapibus ultrices in iaculis Arcu non sodales neque sodales ut etiam sit amet nisl Nibh nisl condimentum id venenatis Lobortis scelerisque fermentum dui faucibus in ornare quam"
    splits = text.split(" ")
    colors = ['#FCBA03', '#0388FC', '#FC032D']
    data = [{'tag': word,
             'weight': randint(1,100),
             'color': np.random.choice(colors, 1)[0]} for word in splits[:50]]
    return {"data": data, 'legend': [{"name": lan, "fill": c} for lan, c in zip(['spanish', 'french', 'russian'], colors)]}


def get_bar_chart(user):
    data = [{
        "subreddit": "r/sub1",
        "spanish": 300,
        "french": 200,
        "russian": 100
    }, {
        "subreddit": "r/sub2",
        "spanish": 20,
        "french": 200,
        "russian": 60
    }, {
        "subreddit": "r/sub3",
        "spanish": 200,
        "french": 20,
        "russian": 50
    }]
    return {"data":data, 'languages': ['spanish', 'french', 'russian'], 'colors': ['#FCBA03', '#0388FC', '#FC032D']}


def get_flash_cards(user):
    cards = [
        {'language': language, 'color': color,
         "words": [{"front": "words", "back": "back"} for __ in range(8)]} for language, color in zip(['spanish', 'french', 'russian'], ['#FCBA03', '#0388FC', '#FC032D'])
    ]
    return cards