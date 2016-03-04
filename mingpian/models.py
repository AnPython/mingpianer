# coding: utf-8

from django.db.models import Model
from django.db.models.fields import CharField, TextField, EmailField, DateTimeField, BooleanField


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

    @property
    def summary(self):
        mingpian_template = u"姓名：{name}\n微信号：{weixin}\n电话：{phone_num}\n" \
                            u"电话2：{phone_num_2}\n邮箱：{email}\n坐标：{address}\n备注：{remark}\n"
        return mingpian_template.format(name=self.name,
                                        weixin=self.weixin,
                                        phone_num=self.phone_number,
                                        phone_num_2=self.phone_number_2,
                                        email=self.email,
                                        address=self.address,
                                        remark=self.remark)
