from flask import Flask, render_template
from reddit_con import get_comment

app = Flask(__name__)


@app.route('/')
def hello_world():
    comment = get_comment(
        url="https://www.reddit.com/r/iPadPro/comments/fduvm7/apple_pencil_help/fjjw1j1?utm_source=share&utm_medium=web2x")
    return render_template("index.html", comments=[comment])


if __name__ == '__main__':
    app.run()
