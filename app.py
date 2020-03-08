from flask import Flask, render_template
from reddit_con import get_comment

app = Flask(__name__)


@app.route('/')
def landing_page():
    comment = get_comment(
        url="https://www.reddit.com/r/iPadPro/comments/fduvm7/apple_pencil_help/fjl0r10?utm_source=share&utm_medium=web2x")
    return render_template("index.html", comments=[comment])


@app.route('/u/<user>')
def user_feed_page(user):
    comment = get_comment(
        url="https://www.reddit.com/r/iPadPro/comments/fduvm7/apple_pencil_help/fjl0r10?utm_source=share&utm_medium=web2x")
    return render_template("gen_feed.html", comments=[comment])

@app.route('/u/<user>/myfeed')
def user_my_feed(user):
    comment = get_comment(
        url="https://www.reddit.com/r/iPadPro/comments/fduvm7/apple_pencil_help/fjl0r10?utm_source=share&utm_medium=web2x")
    return render_template("my_feed.html", comments=[comment])


if __name__ == '__main__':
    app.run()
