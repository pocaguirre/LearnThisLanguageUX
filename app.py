from flask import Flask, render_template, jsonify, request
from fake_data import get_comment, get_table, get_stack_bar, get_word_cloud, get_bar_chart

app = Flask(__name__)


@app.route('/')
def landing_page():
    comment = get_comment(
        url="https://www.reddit.com/r/iPadPro/comments/fduvm7/apple_pencil_help/fjl0r10?utm_source=share&utm_medium=web2x")
    comments = [comment for _ in range(10)]
    return render_template("index.html", comments=comments)


@app.route('/u/<user>')
def user_feed_page(user):
    comment = get_comment(
        url="https://www.reddit.com/r/iPadPro/comments/fduvm7/apple_pencil_help/fjl0r10?utm_source=share&utm_medium=web2x")
    comments = [comment for _ in range(10)]
    return render_template("gen_feed.html", comments=comments)


@app.route('/u/<user>/myfeed')
def user_my_feed(user):
    comment = get_comment(
        url="https://www.reddit.com/r/iPadPro/comments/fduvm7/apple_pencil_help/fjl0r10?utm_source=share&utm_medium=web2x")
    comments = [comment for _ in range(10)]
    columns, data = get_table()
    return render_template("my_feed.html", table_columns=columns, table_data=data, comments=comments)


@app.route('/u/<user>/dashboard')
def user_dashboard(user):
    return render_template("my_dashboard.html")


@app.route('/api/stacked_area', methods=['POST'])
def stacked_area_data():
    user = request.form['user']
    data = get_stack_bar(user)
    return jsonify(data)

@app.route('/api/word_cloud', methods=['POST'])
def word_cloud_data():
    user = request.form['user']
    data = get_word_cloud(user)
    return jsonify(data)

@app.route('/api/bar_chart', methods=['POST'])
def bar_chart_data():
    user = request.form['user']
    data = get_bar_chart(user)
    return jsonify(data)


if __name__ == '__main__':
    app.run()
