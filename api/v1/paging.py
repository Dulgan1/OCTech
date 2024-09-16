from api.v1 import api_view
from app import db_client
from flask import jsonify, request, make_responce, abort
from os import getenv
from pymongo import DESCENDING
import math

def index_range(page: int, page_size: int) -> tuple:
    """The function should return a tuple of size two containing
    a start index and an end index corresponding to the range of
    indexes to return in a list for those particular pagination parameters.
    Page numbers are 1-indexed, i.e. the first page is page 1.
    """
    return ((page * page_size) - page_size, page * page_size)



@api_view.route('/page', strict_slashes=False, methods=['POST'])
def post_paging():
    #if request.get_json():
    p_list = []
    db = db_client[getenv('MAIN_DB')]
#try:
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

    return make_responce(jsonify({'page_size': page_size,
            'page': page,
            'data': p_list,
            'total_pages': int(total_pages),
            'next_page': page + 1 if page < int(total_pages) else None,
            'prev_page': page - 1 if page > 1 else None
            }), 200)
    #except:
        #return make_responce(jsonify({'error': 'an error occured'}), 300)

    #abort(400, 'Missing page data')

@api_view.route('/page/category/<category>', strict_slashes=False, methods=['POST'])
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

            return make_responce(jsonify({'page_size': page_size,
                    'page': page,
                    'data': p_list,
                    'total_pages': int(total_pages),
                    'next_page': page + 1 if page < int(total_pages) else None,
                    'prev_page': page - 1 if page > 1 else None
                    }), 200)
        except:
            return make_responce(jsonify({'error': 'an error occured'}), 300)

    abort(400, 'Missing page data')
