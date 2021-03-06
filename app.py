from flask import Flask, render_template, jsonify, request, session, redirect
import get_data


app = Flask(__name__)
app.secret_key = "secretkey"
db = get_data


@app.route('/')
def landing_page():
    if 'username' in session:
        return redirect("/u/{}".format(session['username']))
    else:
        comments = db.get_all_comments()
        return render_template("landing_page.html", comments=comments)


@app.route('/feed')
def feed():
    if 'username' in session:
        return redirect("/u/{}".format(session['username']))
    else:
        comments = db.get_all_comments()
        return render_template("index.html", comments=comments)


@app.route('/u/<user>')
def user_feed_page(user):
    if 'username' in session and user == session['username']:
        comments = db.get_all_comments()
        user_info = db.get_user_info(session['username'])
        return render_template("gen_feed.html", comments=comments, user=user_info)
    else:
        return redirect("/")


@app.route('/u/<user>/myfeed')
def user_my_feed(user):
    if 'username' in session and user == session['username']:
        comments = db.get_user_comments(user)
        columns, data = db.get_table(user)
        user_info = db.get_user_info(session['username'])
        return render_template("my_feed.html", table_columns=columns, table_data=data, comments=comments, user=user_info)
    else:
        return redirect("/")


@app.route('/u/<user>/dashboard')
def user_dashboard(user):
    if 'username' in session and user == session['username']:
        flashcards = db.get_flash_cards(user)
        user_info = db.get_user_info(session['username'])
        return render_template("my_dashboard.html", cards=flashcards, user=user_info)
    else:
        return redirect("/")


@app.route("/login", methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if db.check_user(username, password):
        session['username'] = username
        return redirect('/u/{}'.format(username))
    return redirect('/')


@app.route("/logout", methods=['GET'])
def logout():
    session.pop('username', None)
    return redirect("/")

@app.route("/signup", methods=['GET', 'POST'])
def initialize_user():
    if request.method == 'GET':
        return render_template("sign_up.html")
    elif request.method == 'POST':
        ## Parse Form Username
        username = request.form['redditid']
        name = request.form['name']
        passwd = request.form['password1']
        db.create_new_user(username=username, name=name, password=passwd)
        print("done creating")
        session['username'] = username
        ## Make Recommendations and Cache In Database
        db.initialize_user_recommendations(username)
        return redirect('/u/{}'.format(username))

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


@app.route('/api/user_lookup', methods=['POST'])
def api_user_lookup():
    user = request.form['user']
    return jsonify({'valid': db.is_user(user)})


if __name__ == '__main__':
    # app.run(host='0.0.0.0')
    app.run()