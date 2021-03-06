from collections import namedtuple
import json


class Tweet(object):
    def __init__(self):
        self.reply_chain = None
        self.annotation = None
        self.thread_annotation = None

    def phemeTweet(self, dict):
        for key, value in dict.items():
            setattr(self, key, value)
            if key == 'user':
                user = User()
                user.phemeUser(value)
                self.user = user
            elif key == 'entities':
                entities = Entities(value)
                self.entities = entities

    def to_dict(self):
        dict = {}
        for key, value in vars(self).items():
            dict[key] = value
        return dict

    def __eq__(self, other):
        return self.text == other.text

    def __str__(self):
        return self.text + ' - ' + self.user.screen_name


class User:
    def phemeUser(self, dict):
        for key, value in dict.items():
            setattr(self, key, value)

    def __str__(self):
        return self.screen_name

    def to_dict(self):
        dict = {}
        for key, value in vars(self).items():
            dict[key] = value
        return dict

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class Entities:
    def __init__(self, dict):
        for key, value in dict.items():
            setattr(self, key, value)

    def to_dict(self):
        dict = {}
        for key, value in vars(self).items():
            dict[key] = value
        return dict

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
