# encoding: utf-8

import re
from hashlib import sha1

from django.views.generic import View
from django.utils.decorators import method_decorator
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from mingpian.models import Mingpian


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

        function_switch, function_type, function_message = self.parse_message(message)
        if function_switch:
            if function_type == 'profile':
                pass #TODO 创建或修改，返回url
            elif self.verify_identity(sender_openid):
                pass #TODO 搜索
            else:
                return HttpResponse(u'您尚未填写名片或未同通过审核，如有问题请联系开发者。')
        else:
            return HttpResponse('')

    @staticmethod
    def extract_message(xml_content):
        sender_openid_re = re.compile(r'<FromUserName><!\[CDATA\[(.+?)\]\]></FromUserName>')
        sender_openid = sender_openid_re.findall(xml_content)[0]
        message_re = re.compile(r'<Content><!\[CDATA\[(.+?)\]\]></Content>')
        message = message_re.findall(xml_content)[0]

        return sender_openid, message.strip()

    @staticmethod
    def parse_message(message):
        if message.lower() == 'p':
            return True, 'profile', None
        elif message.startwith('s'):
            return True, 'search', message[1:].strip()
        else:
            return False, None, None

    @staticmethod
    def verify_identity(openid):
        _object = Mingpian.objects.filter(openid=openid, validity=True)
        if _object.exists():
            return True
        else:
            return False
