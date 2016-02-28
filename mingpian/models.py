# coding: utf-8

from django.db.models import Model
from django.db.models.fields import CharField, TextField, EmailField, DateTimeField, BooleanField
from django.db.models import ForeignKey


class Mingpian(Model):
    openid = CharField(max_length=128, null=True, unique=True)
    name = CharField(max_length=64, db_index=True)
    weixin = CharField(max_length=128, null=True)
    email = EmailField(null=True)
    phone_number = CharField(max_length=64, null=True)
    phone_number_2 = CharField(max_length=64, null=True)
    address = TextField(null=True)
    remark = TextField(null=True)
    last_update = DateTimeField(auto_now=True)
    validity = BooleanField(default=False)

class Philosopherstone(Model):
    code = CharField(max_length=10)
    create_date = DateTimeField(auto_now_add=True)
    player = ForeignKey(Mingpian)
