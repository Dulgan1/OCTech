#!/usr/bin/python3
"""OC Main App"""
from . import db_client
from .api.v1 import api_view
from .models.post import Post
from flask import (Flask, render_template, jsonify,
                   request, session,
                   redirect, url_for,
                   flash, make_response, abort)
from flask_ckeditor import CKEditor
from flask_cors import CORS
import math
from os import getenv
from pymongo import DESCENDING

app = Flask(__name__)
app.register_blueprint(api_view)
app.config['SECRET_KEY'] = getenv('OC_SECRET_KEY')
ckeditor = CKEditor(app)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

def index_range(page: int, page_size: int) -> tuple:
    """The function should return a tuple of size two containing
    a start index and an end index corresponding to the range of
    indexes to return in a list for those particular pagination parameters.
    Page numbers are 1-indexed, i.e. the first page is page 1.
    """
    return ((page * page_size) - page_size, page * page_size)


#=====================================API=====================================#
#                                                                             #

@app.route('/api/page', strict_slashes=False, methods=['POST'])
def post_paging():
    if request.get_json():
        p_list = []
        db = db_client[getenv('MAIN_DB')]

        try:
            data = request.get_json()
            page = data['page']
            page_size = data['page_size']

            assert type(page) is int and page != 0
            assert type(page_size) is int

            start, end = index_range(page, page_size)

            p_posts = db.posts.find(sort=[('index', DESCENDING)]).limit(end - start).skip(start)
            total_pages = math.ceil(db.posts.find().count() / page_size)

            for posts in p_posts:
                p_list.append(posts)
                if '_id' in p_list[-1]:
                    del p_list[-1]['_id']

            return make_response(jsonify({'page_size': page_size, 'page': page, 'data': p_list,
                                         'total_pages': int(total_pages),
                                         'next_page': page + 1 if page < int(total_pages) else None,
                                         'prev_page': page - 1 if page > 1 else None
                                         }), 200)
        except:
            return make_response(jsonify({'error': 'an error occured'}), 300)

    abort(400, 'Missing page data')

@app.route('/api/page/category/<category>', strict_slashes=False, methods=['POST'])
def post_paging_cat(category):
    if request.get_json():
        p_list = []
        db = db_client[getenv('MAIN_DB')]
        try:
            data = request.get_json()
            page = data['page']
            page_size = data['page_size']

            assert type(page) is int and page != 0
            assert type(page_size) is int

            start, end = index_range(page, page_size)

            p_posts = db.posts.find({'cat_list': category}, sort=[('index', DESCENDING)]).limit(end - start).skip(start)
            total_pages = math.ceil(db.posts.find().count() / page_size)

            for posts in p_posts:
                p_list.append(posts)
                if '_id' in p_list[-1]:
                    del p_list[-1]['_id']

            return make_response(jsonify({'page_size': page_size,
                    'page': page,
                    'data': p_list,
                    'total_pages': int(total_pages),
                    'next_page': page + 1 if page < int(total_pages) else None,
                    'prev_page': page - 1 if page > 1 else None
                    }), 200)
        except:
            return make_response(jsonify({'error': 'an error occured'}), 300)

    abort(400, 'Missing page data')

#================================END API======================================#

@app.route('/about', strict_slashes=False)
def about():
    return render_template('about.html')

@app.route('/contact', strict_slashes=False)
def contact():
    return render_template('contact.html')

@app.route('/privacy', strict_slashes=False)
def p_policy():
    return render_template('p_policy.html')


@app.route('/search', strict_slashes=False, methods=['GET', 'POST'])
def search():
    db = db_client[getenv('MAIN_DB')]
    query = request.form.get('query')
    posts = db.posts.find({'$text': {'$search': query}},
                        {'score': {'$meta': 'textScore'}}).sort([('score', {'$meta': 'textScore'})])
    
    return render_template('search.html', posts=posts)

@app.route('/')
def index():
    db = db_client[getenv('MAIN_DB')]
    s_posts = db.posts.find(sort=[('index', DESCENDING)], limit=3)
    if db.posts.find().count() > 12:
        open_posts = db.posts.find(sort=[('index', DESCENDING)], limit=12)
        #.limit(12)
        return render_template('index.html', open_posts=open_posts, s_posts=s_posts)
    else:
        open_posts = db.posts.find(sort=[('index', DESCENDING)])
        # .limit(db.posts.find({{'category': category}}).count())
        return render_template('index.html', open_posts=open_posts, s_posts=s_posts)


@app.route('/admin', methods=['GET', 'POST'],
                strict_slashes=False)
def admin():
    if request.method == 'GET':
        if not session.get('user_name'):
            return redirect(url_for('admin_login'))
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
        image_url = request.form.get('image_url')
        cat_list = request.form.get('cat_list')
        index = post_db.posts.find().count() + 1
        title = request.form['title']
        cleaned_title = title.replace('/', '').\
            replace('&', '').replace('~', '').replace('!', '').replace('.', '')
        route = ('-').join((f'{cleaned_title} {index}').split())
        tags = request.form.get('tags').split(',')

        new_post = Post(posted_by=posted_by, content=content, tags=tags,
                    image_url=image_url, index=index, title=title,
                    route=route, dex=dex, cat_list=cat_list)
        post_db.posts.insert(new_post.to_dict())
        error = 'Successfully posted blog'

        return render_template('admin.html', error=error)

    except Exception as e:
        session['ckeditor'] = request.form.get('ckeditor')
        session['image_url'] = request.form.get('image_url')
        session['dex'] = request.form.get('dex')
        session['title'] = request.form.get('title')
        session['tags'] = request.form.get('tags')
        session['cat_list'] = request.form.get('cat_list')

        error = f'AN ERROR OCCURED: Could not add new post {e}'

        return render_template('admin.html', error=error,
                                content=session['ckeditor'],
                                title=session['title'],
                                image_url=session['image_url'],
                                tags=session['tags'],
                                description=session['dex'],
                                category=session['cat_list'])

@app.route('/admin/login', methods=['GET', 'POST'],
                strict_slashes=False)
def admin_login():

    if request.method == 'POST':
        user_name = request.form.get('user_name')
        session['user_name'] = user_name
        password = request.form.get('password')

        if user_name == 'Admin' and password == getenv('OC_SECRET_KEY'):
            return redirect(url_for('admin'))

    return render_template('login.html')
    """
    # THE CODE BELOW IS FOR TESTING PURPOSE ONLY
    session['user_name'] = 'Admin'
    return redirect(url_for('app_view.admin')"""

@app.route('/post/<post_route>', methods=['GET'], strict_slashes=False)
def post(post_route):
    try:
        mon_ = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        db = db_client[getenv('MAIN_DB')]
        blog_post = db.posts.find_one({'route': post_route})
        related_post = db.posts.find({'cat_list': blog_post.get('cat_list')}, sort=[('index', DESCENDING)], limit=7)
        created_time = blog_post.get('created_at').split('T')[1].split(':')
        blog_post['created_time'] = created_time
        create_date = blog_post.get('created_at').split('T')[0].split('-')
        create_date[1] = mon_[int(create_date[1]) - 1]
        blog_post['created_date'] = create_date
            
        return render_template('single-standard.html', blog_post=blog_post, related_post=related_post) \
                    if blog_post else render_template('404.html')
    except Exception as e:
        flash(f'AN ERROR OCCURED: {e}')
        return redirect(url_for('.index'))

@app.route('/category/<category>', strict_slashes=False, methods=['GET'])
def category(category):
    db = db_client[getenv('MAIN_DB')]
    if db.posts.find({'cat_list': category}).count() > 12:
        cat_posts = db.posts.find({'cat_list': category}, sort=[('index', DESCENDING)], limit=12)
        #.limit(12)
        return render_template('category.html', cat_posts=cat_posts, category=category)
    else:
        cat_posts = db.posts.find({'cat_list': category}, sort=[('index', DESCENDING)])
        # .limit(db.posts.find({{'category': category}}).count())
        return render_template('category.html', cat_posts=cat_posts, category=category)


@app.teardown_appcontext
def close_storage(error):
    """ Closes database storage connection on error"""
    db_client.close()


@app.errorhandler(404)
def error404(error):
    """ Error hanlder for 404 """
    return render_template('404.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')