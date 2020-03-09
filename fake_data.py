from praw import Reddit
from praw.models.reddit.comment import Comment
from datetime import datetime
import natural.date as dt
import time

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
    return {'data': data, 'languages': ['spanish', 'french', 'russian']}


def get_word_cloud(user):
    data = [{
        "tag": "Breaking News",
        "weight": 60,
        "color": "#4A2040"
    }, {
        "tag": "Environment",
        "weight": 80,
        "color": "#9F6BA0"
    }, {
        "tag": "Politics",
        "weight": 90,
        "color": "#C880B7"
    }, {
        "tag": "Business",
        "weight": 25,
        "color": "#EC9DED"
    }, {
        "tag": "Lifestyle",
        "weight": 30,
        "color": "#DFBAD3"
    }, {
        "tag": "World",
        "weight": 45,
        "color": "#C880B7"
    }, {
        "tag": "Sports",
        "weight": 160,
        "color": "#34D2EB"
    }, {
        "tag": "Fashion",
        "weight": 20,
        "color": "#C880B7"
    }, {
        "tag": "Education",
        "weight": 78,
        "color": "#9F6BA0"
    }]
    return data


def get_bar_chart(user):
    data = [{
        "country": "USA",
        "visits": 3025
        }, {
          "country": "China",
          "visits": 1882
        }, {
          "country": "Japan",
          "visits": 1809
        }]
    return data