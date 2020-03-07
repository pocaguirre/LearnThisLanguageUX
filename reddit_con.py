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
    trans_obj = {'translated': {}, 'parent': {},'request': {}}

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
        trans_obj['parent']['body'] = parent.flair.selftext_html
        trans_obj['parent']['title'] = parent.flair.title
        trans_obj['parent']['points'] = parent.flair.score
        trans_obj['parent']['author'] = parent.flair.author.name
        trans_obj['parent']['url'] = parent.flair.url
        trans_obj['parent']['time'] = dt.duration(datetime.fromtimestamp(parent.flair.created),
                                                  now=datetime.fromtimestamp(time.time()))
    trans_obj['footer']['url'] = parent.flair.url
    trans_obj['footer']['title'] = 
    return trans_obj
