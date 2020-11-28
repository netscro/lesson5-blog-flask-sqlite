from flask import Flask, render_template, request, redirect
import sqlite3
import datetime
app = Flask(__name__)

"""
command to create database
CREATE TABLE post (Id INTEGER PRIMARY KEY AUTOINCREMENT, title varchar(100), description varchar(200), date INTEGER);
"""


@app.route('/')
def index():
    """
    Home page. Prints the all posts in blog.
    :return: all posts in blog
    """
    connection = sqlite3.connect('blog.sqlite')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM posts")
    blog_posts = cursor.fetchall()
    connection.close()
    return render_template('index.html', blog_posts=blog_posts)


@app.route('/addpost')
def addpost():
    """
    The page for adding a new blog post via variables in url.
    title = post title, description = short description of the post.
    :return: home page with new post
    """
    # берем параметры из url для title и description
    post_title = request.args.get('title')
    post_description = request.args.get('description')
    # добавляяем вывод ошибки если не ввели title
    if not post_title:
        return '<h1>Ошибка. Вы не ввели название поста "title"</>'

    elif not post_description:
        return '<h1>Ошибка. Вы не ввели описание поста "description"</>'

    # берем текущую дату
    local_time = datetime.datetime.now()
    # убираем миллисекунды
    date_post = local_time.strftime('%Y-%m-%d %H:%M:%S')
    # передаем параметры из url
    add_values = (None, post_title, post_description, date_post)
    connection = sqlite3.connect('blog.sqlite')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO posts (Id, title, description, date) VALUES (?, ?, ?, ?)', add_values)
    connection.commit()
    connection.close()
    # редиректим на главную страницу
    return redirect('/')


@app.route('/delete')
def delete():
    """
    This page delete post via variables in url.
    id = post id which needs to be removed
    :return: home page, prints all posts without delete post
    """
    post_id = request.args.get('id')
    connection = sqlite3.connect('blog.sqlite')
    if not post_id:
        return '<h1>Ошибка. Вы не ввели номер поста "id"</>'
    cursor = connection.cursor()
    cursor.execute('DELETE FROM posts WHERE Id = ?', post_id)
    connection.commit()
    connection.close()
    return redirect('/')


@app.route('/update')
def update():
    """
    This page update post via variables in url.
    id = id of post which need update.
    title = post title, description = short description of the post.
    :return: home page, prints all posts with updated post and update date
    """
    post_id = request.args.get('id')
    post_title = request.args.get('title')
    post_description = request.args.get('description')
    if not post_id:
        return '<h1>Ошибка. Вы не ввели номер поста "id"</>'

    if not post_title:
        return '<h1>Ошибка. Вы не ввели название поста "title"</>'

    elif not post_description:
        return '<h1>Ошибка. Вы не ввели описание поста "description"</>'

    connection = sqlite3.connect('blog.sqlite')
    cursor = connection.cursor()
    # обновляем дату измененного поста
    local_time = datetime.datetime.now()
    # убираем миллисекунды
    date_post = local_time.strftime('%Y-%m-%d %H:%M:%S')
    add_values = (post_title, post_description, date_post, post_id)
    cursor.execute("UPDATE posts SET title = ?, description = ?, date = ? WHERE ID = ?", add_values)
    connection.commit()
    connection.close()
    # редиректим на главную страницу
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
