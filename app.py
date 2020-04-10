from flask import Flask, render_template, jsonify, request, session, redirect
import get_data
import fake_data

## This variable is to use fake data
fake = False


app = Flask(__name__)
app.secret_key = "secretkey"
if fake:
    db = fake_data
else:
    db = get_data


@app.route('/')
def landing_page():
    if 'username' in session:
        return redirect("/u/{}".format(session['username']))
    else:
        if fake:
            comment = db.get_comment(
                url="https://www.reddit.com/r/iPadPro/comments/fduvm7/apple_pencil_help/fjl0r10?utm_source=share&utm_medium=web2x")
            comments = [comment for _ in range(10)]
        else:
            comments = db.get_all_comments()
        return render_template("index.html", comments=comments)


@app.route('/u/<user>')
def user_feed_page(user):
    if 'username' in session:
        if fake:
            comment = db.get_comment(
                url="https://www.reddit.com/r/iPadPro/comments/fduvm7/apple_pencil_help/fjl0r10?utm_source=share&utm_medium=web2x")
            comments = [comment for _ in range(10)]
            user_info = {'username':"JSmithUser", "name": "John Smith"}
        else:
            comments = db.get_all_comments()
            user_info = db.get_user_info(session['username'])
        return render_template("gen_feed.html", comments=comments, user=user_info)
    else:
        return redirect("/")


@app.route('/u/<user>/myfeed')
def user_my_feed(user):
    if fake:
        comment = db.get_comment(
            url="https://www.reddit.com/r/iPadPro/comments/fduvm7/apple_pencil_help/fjl0r10?utm_source=share&utm_medium=web2x")
        comments = [comment for _ in range(10)]
        columns, data = db.get_table()
        user_info = {'username': "JSmithUser", "name": "John Smith"}
    else:
        comments = db.get_user_comments(user)
        columns, data = db.get_table(user)
        user_info = db.get_user_info(session['username'])
    return render_template("my_feed.html", table_columns=columns, table_data=data, comments=comments, user=user_info)


@app.route('/u/<user>/dashboard')
def user_dashboard(user):
    flashcards = db.get_flash_cards(user)
    user_info = db.get_user_info(session['username'])
    return render_template("my_dashboard.html", cards=flashcards, user=user_info)


@app.route("/login", methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if db.check_user(username, password):
        session['username'] = username
        return redirect('/u/{}'.format(username))
    return render_template('index.html')

@app.route("/sign-up", methods=['POST'])
def initialize_user():
    ## Parse Form Username
    username = request.form['username']
    ## Make Recommendations and Cache In Database
    _ = db.initialize_user_recommendations(username)

@app.route('/api/stacked_area', methods=['POST'])
def stacked_area_data():
    user = request.form['user']
    data = db.get_stack_bar(user)
    return jsonify(data)

@app.route('/api/word_cloud', methods=['POST'])
def word_cloud_data():
    user = request.form['user']
    data = db.get_word_cloud(user)
    return jsonify(data)

@app.route('/api/bar_chart', methods=['POST'])
def bar_chart_data():
    user = request.form['user']
    data = db.get_bar_chart(user)
    return jsonify(data)


@app.route('/api/recommendations', methods=['POST'])
def recommendations():
    user = request.form['user']
    columns, data = db.get_recommendations(user)
    return jsonify(data)


if __name__ == '__main__':
    app.run()
