#!/usr/bin/env python3
from datetime import datetime

class Post():
    """Class for blog post
    attributes:
        posted_by: str
        content: str
        image_url: str
        dex: str # dscription
        index: int = 0
        route: str
        title: str
        tags: list
    """

    def __init__(self, *args, **kwargs):
        if kwargs:
            for k, v in kwargs.items():
                if k != '__class__':
                    setattr(self, k, v)
        self.created_at = datetime.now()

    def to_dict(self) -> dict:
        """Returns a dictionary of class instance"""
        temp = self.__dict__.copy()
        temp['created_at'] = datetime.isoformat(temp['created_at'])
        temp['__class__'] = self.__class__.__name__
        if '_sa_instance_state' in temp:
            del temp['_sa_instance_state']
        return temp
