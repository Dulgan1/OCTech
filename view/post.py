from flask import redirect, url_for, render_template, flash
from view import app_view, db_client
from os import getenv


@app_view.route('/post/<post_route>', methods=['GET'], strict_slashes=False)
def post(post_route):
    try:
        db = db_client[getenv('MAIN_DB')]
        blog_post = db.posts.find_one({'route': post_route})

        return render_template('post.html', blog_post=blog_post) \
            if blog_post else render_template('404.html')
    except Exception as e:
        flash(f'AN ERROR OCCURED: {e}')
        return redirect(url_for('app_view.index'))
