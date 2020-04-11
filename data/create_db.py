import mysql.connector
import json
from mysql.connector import errorcode

with open("./db_config.json", 'r') as fp:
    db_config = json.load(fp)


TABLES = {}
TABLES['UserRecommendedSubreddit'] = (
    "CREATE TABLE IF NOT EXISTS `UserRecommendedSubreddits` ("
        "`user_id`       VARCHAR(255) NOT NULL,"
        "`subreddit_id`  VARCHAR(255) NOT NULL,"
        "`rec_score`     REAL NOT NULL,"
        "PRIMARY KEY(`user_id`,`subreddit_id`)"
    ");"
)

TABLES["UserCommentHistory"] = (
    "CREATE TABLE IF NOT EXISTS `UserCommentHistory` ("
        "`user_id`       VARCHAR(255) NOT NULL,"
        "`subreddit_id`  VARCHAR(255) NOT NULL,"
        "`comments_cnt`  INTEGER NOT NULL,"
        "PRIMARY KEY(`user_id`,`subreddit_id`)"
    ");"
)

TABLES["SubredditLanguageStats"] = (
    "CREATE TABLE IF NOT EXISTS `SubredditLanguageStats` ("
        "`subreddit_id`  VARCHAR(255) NOT NULL,"
        "`lang_id`       VARCHAR(255) NOT NULL,"
        "`posts_cnt`     INTEGER NOT NULL,"
        "PRIMARY KEY(`subreddit_id`,`lang_id`)"
    ");"
)

TABLES["UserLearnProgress"] = (
    "CREATE TABLE IF NOT EXISTS `UserLearnProgress` ("
        "`user_id`       VARCHAR(255) NOT NULL,"
        "`src_lang_word` VARCHAR(255) NOT NULL,"
        "`tgt_lang_word` VARCHAR(255) NOT NULL,"
        "`word_status`   INTEGER NOT NULL,"
        "`src_lang_id`   VARCHAR(255) NOT NULL,"
        "`tgt_lang_id`   VARCHAR(255) NOT NULL,"
        "PRIMARY KEY(`user_id`,`src_lang_word`,`tgt_lang_word`,`src_lang_id`,`tgt_lang_id`)"
    ");"
)

TABLES['Users'] = (
    "CREATE TABLE IF NOT EXISTS `Users` ("
        "`username`     VARCHAR(255) NOT NULL,"
        "`name`         TEXT,"
        "`passwd`       VARCHAR(255) NOT NULL,"
        "PRIMARY KEY(`username`)"
    ");"
)

TABLES['SourceComment'] = (
    "CREATE TABLE IF NOT EXISTS `SourceComment` ("
        "`comment_id`   VARCHAR(255) NOT NULL,"
        "`author_id`    TEXT NOT NULL,"
        "`title`        TEXT,"
        "`body`         TEXT NOT NULL,"
        "`points`       TEXT NOT NULL,"
        "`url`          TEXT NOT NULL,"
        "`time`         DATETIME NOT NULL,"
        "`lang_id`      BLOB NOT NULL,"
        "PRIMARY KEY(`comment_id`)"
    ");"
)


TABLES['TargetComment'] = (
    "CREATE TABLE IF NOT EXISTS `TargetComment` ("
        "`comment_id`               VARCHAR(255) NOT NULL,"
        "`author_id`                TEXT NOT NULL,"
        "`body`                     TEXT NOT NULL,"
        "`points`                   TEXT NOT NULL,"
        "`url`                      TEXT NOT NULL,"
        "`time`                     DATETIME NOT NULL,"
        "`lang_id`                  BLOB NOT NULL,"
        "`request_comment_id`       TEXT NOT NULL,"
        "`request_author_id`        TEXT NOT NULL,"
        "`request_body`             TEXT NOT NULL,"
        "`request_points`           TEXT NOT NULL,"
        "`request_url`              TEXT NOT NULL,"
        "`request_time`             DATETIME NOT NULL,"
        "`submission_url`           TEXT NOT NULL,"
        "`submission_title`         TEXT NOT NULL,"
        "`submission_subreddit_id`  TEXT NOT NULL,"
        "`submission_points`        TEXT NOT NULL,"
        "`submission_comment_cnt`   TEXT NOT NULL,"
        "`source_comment_id`        TEXT NOT NULL,"
        "PRIMARY KEY(`comment_id`)"
    ");"
)


def get_con():
    con = mysql.connector.connect(host=db_config['host'],
                                  user=db_config['user'],
                                  passwd=db_config['passwd'],
                                  db=db_config['db'])
    return con


def set_up_db():
    cnx = mysql.connector.connect(host=db_config['host'],
                                  user=db_config['user'],
                                  passwd=db_config['passwd'])
    cursor = cnx.cursor()
    print("Creating database {}: ".format(db_config['db']), end='')
    cursor.execute("CREATE DATABASE IF NOT EXISTS {};".format(db_config['db']))
    print("OK")

    con = get_con()
    cur = con.cursor()
    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print("Creating table {}: ".format(table_name), end='')
            cur.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

    cur.close()
    con.close()




if __name__ == '__main__':
    set_up_db()
