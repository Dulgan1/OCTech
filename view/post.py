from flask import redirect, url_for, render_template, flash
import ijson
from os import getenv
from view import app_view, db_client


@app_view.route('/post/<post_route>', methods=['GET'], strict_slashes=False)
def post(post_route):
    try:
        if getenv('OC_DBT') == 'db':
            db = db_client[getenv('MAIN_DB')]
            blog_post = db.posts.find_one({'route': post_route})

            return render_template('post.html', blog_post=blog_post) \
                if blog_post else render_template('404.html')
        else:
            with open('../db/data.json', 'wrb') as f_db:
            #TODO: Finish data loading from json using ijson
    except Exception as e:
        flash(f'AN ERROR OCCURED: {e}')
        return redirect(url_for('app_view.index'))
