import praw
import time
import re
import pickle
import get_data
from language_codes import lang2codex, codex2lang #local file w/language code mappings
from googletrans import Translator

# -- reddit service --
r = praw.Reddit(client_id='bvhChMkziTUTMQ',
                client_secret='OThqRFN-zNDRobV-xJBBNGyMQIs',
                password='aisys&design',
                user_agent='learnthislanguagebot 1.0',
                username='LearnThisLanguageBot')

keywords = ['TeachMeANewLanguage']
regkey   = '(?:% s)' % '|'.join(keywords)

sublist    = ["LearnALanguageBooks","LearnALanguageSports"]
subreddits = [r.subreddit(x) for x in sublist]

cur, conn = get_data.get_db()

cur.execute('select request_comment_id as rcid from TargetComment')
past_requests = {row['rcid'] for row in cur.fetchall()}

# -- translate post --
mt = Translator()
print('%d languages supported' % len(lang2codex))
print(23*'-')

def translate_post(comment_text, src_text):
    # get and map language src & tgt
    lang = comment_text.strip().split()[-1].lower() #expects only 1 language per comment
    code = lang2codex[lang]

    # translate & compose
    hyp = mt.translate(src_text,dest=code) #src inferred using lid if not provided

    prefix = 'I think a good way to say this in %s might be: \n> %s' % (codex2lang[hyp.dest].capitalize(),hyp.text)
    pron   = 'pronounced: \n> "%s"' % hyp.pronunciation if hyp.pronunciation!=None else ''
    suffix = 'Have a better translation? Let me know in a comment below!\n\nInterested in learning a new language? Sign up and track your progress at [learnthislanguage.me](http://learnthislanguage.me)'

    return '\n'.join([prefix,pron,suffix]), code


# -- bot runner --
def run_bot():
    import inspect
    for subreddit in subreddits:
        comments  = subreddit.comments(limit=None)
        for comment in comments:
            comment_text = comment.body.lower()

            # if haven't already replied to post
            if comment.id not in past_requests:
                # check for key(s), not case-sensitive
                if re.search(regkey, comment_text, re.IGNORECASE):
                    print("yay! ",comment.id)
                    # get parent comment to translate and post
                    # different fields for posts vs comments
                    if type(comment.parent()) == praw.models.reddit.comment.Comment:
                        src_text = comment.parent().body.lower()
                        to_post, lang_id = translate_post(comment_text, src_text)
                    else:
                        if comment.parent().selftext == '':
                            # No text body
                            continue
                        else:
                            src_text = comment.parent().selftext #terrible name scheme
                            to_post, lang_id = translate_post(comment_text, src_text)
                    # post & add comment id to cache
                    new_comment = comment.reply(to_post)
                    if new_comment is not None:
                        get_data.cache_comment(cur, id=new_comment.id, lang_id=lang_id)
                        past_requests.add(comment.id)

    conn.commit()


while True:
    run_bot()
    time.sleep(10)
