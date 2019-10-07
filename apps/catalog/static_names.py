# -*- coding: utf-8 -*-
class Color(object):
    """Colors"""
    OTHER = 99
    color_rus = {
        u'красный': 1,
        u'розовый': 2,
        u'зеленый': 3,
        u'голубой': 4,
        u'фиолетовый': 5,
        u'белый': 6,
        u'черный': 7,
        u'желтый': 8,
        u'коричневый': 9,
        u'серый': 10,
        u'бежевый': 11,
        u'оранжевый': 12,
        u'cиний': 13,
        u'разноцветные': OTHER
    }

    color_eng = {
        u'red': 1,
        u'pink': 2,
        u'green': 3,
        u'purple': 5,
        u'white': 6,
        u'black': 7,
        u'yellow': 8,
        u'brown': 9,
        u'grey': 10,
        u'beige': 11,
        u'orange': 12,
        u'blue': 13,
        u'other': OTHER
    }

    reverse_color = {v: k for k, v in color_rus.items()}

    @classmethod
    def get_name(cls, id):
        """
            Return color name
        """
        if isinstance(id, basestring):
            try:
                id = int(id)
            except ValueError:
                return
        return cls.reverse_color.get(id)

    @classmethod
    def get_id(cls, name):
        """
            Return color id
        """
        if cls.color_rus.get(name):
            return cls.color_rus.get(name)
        if cls.color_eng.get(name):
            return cls.color_eng.get(name)
        return cls.OTHER
