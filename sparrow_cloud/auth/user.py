# -*- coding: utf-8 -*-


class UserBase(object):
    '''自定义的 User 对象'''
    def __init__(self, user_id):
        self._id = user_id

    @property
    def is_authenticated(self):
        return True

    @property
    def id(self):
        return self._id


class User(UserBase):
    def __init__(self, user_id, payload):
        super().__init__(user_id)
        self._payload = payload

    @property
    def payload(self):
        return self._payload