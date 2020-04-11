import mysql.connector
from mysql.connector import errorcode
import pandas as pd
from create_db import db_config, get_con, set_up_db

TABLES = {}
# TABLES['UserRecommendedSubreddits'] = (
#     "LOAD DATA LOCAL INFILE 'data/UserRecommendedSubreddit.csv'"
#     "INTO TABLE `UserRecommendedSubreddits`"
#     "FIELDS TERMINATED BY ','"
#     "ENCLOSED BY '\"'"
#     "LINES TERMINATED BY '\n'"
#     "IGNORE 1 ROWS"
#     "(`user_id`, `subreddit_id`, `rec_score`);"
# )
#
#
# TABLES['UserCommentHistory'] = (
#     "LOAD DATA LOCAL INFILE 'data/UserCommentHistory.csv'"
#     "INTO TABLE `UserCommentHistory`"
#     "FIELDS TERMINATED BY ','"
#     "ENCLOSED BY '\"'"
#     "LINES TERMINATED BY '\n'"
#     "IGNORE 1 ROWS"
#     "(`user_id`, `subreddit_id`, `comments_cnt`);"
# )
#
# TABLES['UserLearnProgress'] = (
#     "LOAD DATA LOCAL INFILE 'data/UserLearnProgress.csv'"
#     "INTO TABLE `UserLearnProgress`"
#     "FIELDS TERMINATED BY ','"
#     "ENCLOSED BY '\"'"
#     "LINES TERMINATED BY '\n'"
#     "IGNORE 1 ROWS"
#     "(`user_id`, `src_lang_word`, `tgt_lang_word`, `word_status`, `src_lang_id`, `tgt_lang_id`);"
# )
#
# TABLES['SubredditLanguageStats'] = (
#     "LOAD DATA LOCAL INFILE 'data/SubredditLanguageStats.csv'"
#     "INTO TABLE `SubredditLanguageStats`"
#     "FIELDS TERMINATED BY ','"
#     "ENCLOSED BY '\"'"
#     "LINES TERMINATED BY '\n'"
#     "IGNORE 1 ROWS"
#     "(`subreddit_id`, `lang_id`, `posts_cnt`);"
# )

TABLES['Users'] = (
    "INSERT INTO `Users` (`username`, `name`, `passwd`) VALUES (%s, %s, %s)"
)


def main():
    con = get_con()
    cur = con.cursor()
    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print("Adding data to table {}: ".format(table_name), end='')
            cur.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

    cur.close()
    con.commit()
    con.close()


if __name__ == '__main__':
    # set_up_db()
    main()
