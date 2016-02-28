# encoding: utf-8

import re
from hashlib import sha1

from django.views.generic import View
from django.utils.decorators import method_decorator
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name='dispatch')
class ReceiveView(View):

    def get(self, request):
        '''
        验证服务器地址有效性
        '''
        try:
            signature = request.GET['signature']
            timestamp = request.GET['timestamp']
            nonce = request.GET['nonce']
            echostr = request.GET['echostr']
        except KeyError:
            return HttpResponse('something wrong')

        token = settings.MY_TOKEN

        array = [token, timestamp, nonce]
        array.sort()
        tmp_str = sha1(''.join(array)).hexdigest()

        if tmp_str == signature:
            return HttpResponse(echostr)
        else:
            return HttpResponse('something wrong')

    def post(self, request):

        xml_content = request.body
        sender_openid, message = self.extract_message(xml_content)
        return HttpResponse('')

    @staticmethod
    def extract_message(xml_content):

        sender_openid_re = re.compile(r'<FromUserName><!\[CDATA\[(.+?)\]\]></FromUserName>')
        sender_openid = sender_openid_re.findall(xml_content)[0]

        message_re = re.compile(r'<Content><!\[CDATA\[(.+?)\]\]></Content>')
        message = message_re.findall(xml_content)[0]

        return sender_openid, message
