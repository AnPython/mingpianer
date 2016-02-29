# coding: utf-8

from django.forms import forms, fields


class MingpianForm(forms.Form):
    name = fields.CharField(max_length=128, required=True, label='名字')
    weixin = fields.CharField(max_length=64, required=False, label='微信号')
    email = fields.EmailField(required=False, label='邮箱')
    phone_number = fields.CharField(max_length=64, required=False, label='电话')
    phone_number_2 = fields.CharField(max_length=64, required=False, label='电话2')
    address = fields.Field(required=False, label='坐标')
    remark = fields.Field(required=False, label='备注')
