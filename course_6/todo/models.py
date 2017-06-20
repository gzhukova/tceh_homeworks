# -*- coding: utf-8 -*-

__author__ = 'sobolevn'

from utils import get_input_function


class Storage(object):  # storage = Storge()
    obj = None

    items = None

    @classmethod
    def __new__(cls, *args):
        if cls.obj is None:
            cls.obj = object.__new__(cls)
            cls.items = []
        return cls.obj


class BaseItem(object):
    def __init__(self, heading):
        self.heading = heading
        self.status = False

    def __repr__(self):
        return self.__class__

    @classmethod
    def construct(cls):
        raise NotImplemented()

    def __str__(self):
        """
        Переопределение статуса объекта
        :return: "+" или "-"
        """
        if self.status:
            return  " +"
        else:
            return " -"

class ToDoItem(BaseItem):
    def __str__(self):
        return 'ToDo: {}'.format(
            self.heading
        ) + super().__str__()

    @classmethod
    def construct(cls):
        input_function = get_input_function()
        heading = input_function('Input heading: ')
        return ToDoItem(heading)


class ToBuyItem(BaseItem):
    def __init__(self, heading, price):
        super(ToBuyItem, self).__init__(heading)
        self.price = price
        self.status = False

    def __str__(self):
        return 'ToBuy: {} for {}'.format(
            self.heading,
            self.price,
        ) + super().__str__()

    @classmethod
    def construct(cls):
        input_function = get_input_function()
        heading = input_function('Input heading: ')
        price = input_function('Input price: ')
        return ToBuyItem(heading, price)


class ToReadItem(BaseItem):

    def __init__(self, title, url):
        self.title = title
        self.url = url
        self.status = False

    def __str__(self):
        return "ToRead: {0} - {1}".format(self.title, self.url) + super().__str__()

    @classmethod
    def construct(cls):
        input_function = get_input_function()
        title = input_function('Input title: ')
        url = input_function('Input url: ')
        return ToReadItem(title, url)

