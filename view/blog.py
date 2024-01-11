from view import app_view, db_client
from models.post import Post
from flask import (request, render_template, session,
                   redirect, url_for)
from os import getenv


@app_view.route('/')
def index():
    return render_template('blog.html')


@app_view.route('/admin', methods=['GET', 'POST'],
                strict_slashes=False)
def admin():
    if request.method == 'GET':
        try:
            content = session['ckeditor'].replace('\r\n', '').replace('\n', '')
            image_url = session['image_url']
            dex = session['dex']
            title = session['title']

            return render_template('admin.html', content=content, title=title,
                                   image_url=image_url)
        except Exception as e:
            return render_template('admin.html')

    try:
        post_db = db_client[getenv('MAIN_DB')]
        posted_by = session['user_name']
        content = request.form.get('ckeditor')
        dex = request.form.get('dex')
        image_url = request.form['image_url']
        index = post_db.posts.find().count() + 1
        title = request.form['title']
        cleaned_title = title.replace('/', '').\
            replace('&', '').replace('~', '').replace('!', '')
        route = ('-').join((f'{cleaned_title} {index}').split())
        tags = request.form.get('tags').split(',')

        new_post = Post(posted_by=posted_by, content=content, tags=tags,
                        image_url=image_url, index=index, title=title,
                        route=route, dex=dex)
        post_db.posts.insert(new_post.to_dict())
        error = 'Successfully posted blog'

        return render_template('admin.html', error=error)

    except Exception as e:
        session['ckeditor'] = request.form.get('ckeditor')
        session['image_url'] = request.form.get('image_url')
        session['dex'] = request.form.get('dex')
        session['title'] = request.form.get('title')
        session['tags'] = request.form.get('tags')
        error = f'AN ERROR OCCURED: Could not add new post {e}'

        return render_template('admin.html', error=error,
                               content=session['ckeditor'],
                               title=session['title'],
                               image_url=session['image_url'],
                               tags=session['tags'])


@app_view.route('/admin/login', methods=['GET', 'POST'],
                strict_slashes=False)
def admin_login():

    """if request.method == 'POST':
        user_name = request.form.get('user_name')
        password = request.form.get('password')

    return render_template('login.html')"""
    # THE CODE BELOW IS FOR TESTING PURPOSE ONLY
    session['user_name'] = 'Admin'
    return redirect(url_for('app_view.admin'))
