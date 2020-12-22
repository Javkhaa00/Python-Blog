from flask import Flask, render_template, request, redirect, url_for, session, escape
import sqlite3

app = Flask(__name__)
app.secret_key = 'OfRu5cqfJr9NGfRbaAZEaKGKvYWtgm5MxCdUVEQS'


@app.route('/')
def all_posts():
    name = None
    if 'loggedin' in session:
        name = session['username']
    con = sqlite3.connect('./test.db')
    c = con.cursor()
    data = c.execute('SELECT id, title FROM post')
    items = []
    for item in data.fetchall():
        dataItem = {
            'id': str(item[0]),
            'title': item[1]
        }
        items.append(dataItem)
    return render_template('all_posts.j2.html', items=items, name=name)


@app.route('/post/<int:post_id>')
def post(post_id):
    conn = sqlite3.connect('./test.db')

    c = conn.cursor()
    c.execute('SELECT * FROM post WHERE id = ' + str(post_id) + ' LIMIT 1')
    data = c.fetchone()
    if data:
        post = {
            'title': data[1],
            'body': data[2]
        }
        return render_template('post.j2.html', post=post)
    return render_template('not_found.j2.html')


@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    if request.method == 'GET':
        return render_template('upload.j2.html')
    elif request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        print(title, desc)

        conn = sqlite3.connect('./test.db')
        c = conn.cursor()
        c.execute(
            'INSERT INTO post (title, body, date) VALUES (?, ?, date())', (title, desc))
        conn.commit()
        conn.close()
        return redirect(url_for('all_posts'))
    else:
        return render_template('not_found.j2.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'GET':
        return render_template('sign_up.j2.html')
    elif request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        confirmPassword = request.form['confirm-password']

        if (password == confirmPassword):
            conn = sqlite3.connect('./test.db')
            c = conn.cursor()
            c.execute(
                'INSERT INTO users (name, password, date) VALUES (?, ?, date())', (name, password))
            conn.commit()
            conn.close()

            return redirect(url_for('signin'))
        else:
            print('NOT WORKING !!!!!!!!!!!!!!!!')
            return render_template('not_found.j2.html')
    else:
        return render_template('not_found.j2.html')


@app.route('/signin', methods=['POST', 'GET'])
def signin():
    if request.method == 'GET':
        return render_template('sign_in.j2.html')
    else:
        name = request.form['name']
        password = request.form['password']

        conn = sqlite3.connect('./test.db')
        c = conn.cursor()
        c.execute(
            'SELECT name, password FROM users WHERE name = ? LIMIT 1', (name,))
        data = c.fetchone()

        login_name = data[0]

        if password == data[1]:
            session['username'] = request.form['name']
            session['loggedin'] = True
            return redirect(url_for('all_posts'))
        else:
            return render_template('not_found.j2.html')

        return redirect(url_for('all_posts'))


app.run(debug=True)
