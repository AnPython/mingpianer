# coding: utf-8

from django.db.models import Model
from django.db.models.fields import CharField, TextField, EmailField, DateTimeField, BooleanField
from django.db.models import ForeignKey
import random


class Mingpian(Model):
    openid = CharField(max_length=128, null=True, unique=True)
    name = CharField(max_length=64, null=True, db_index=True)
    weixin = CharField(max_length=128, null=True)
    email = EmailField(null=True)
    phone_number = CharField(max_length=64, null=True)
    phone_number_2 = CharField(max_length=64, null=True)
    address = TextField(null=True)
    remark = TextField(null=True)
    last_update = DateTimeField(auto_now=True)
    validity = BooleanField(default=False)


class Philosopherstone(Model):
    code = CharField(max_length=10, unique=True)
    create_datetime = DateTimeField(auto_now_add=True)
    player = ForeignKey(Mingpian)

    def save(self, **kwargs):
        # generate code
        code_len = 10
        raw_words = 'abcdefghijklmnopqrstuvwxyz0123456789'
        _code = ''
        for i in range(code_len):
            random_num = random.randint(0, len(raw_words)-1)
            _code += raw_words[random_num]
        self.code = _code
        
        super(Philosopherstone, self).save(**kwargs)
