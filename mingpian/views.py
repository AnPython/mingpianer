# coding: utf-8

from django.conf import settings
from django.shortcuts import HttpResponse
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail

from .models import Mingpian
from .forms import MingpianForm
from mingpianer.utils import redis


class SharedTemplateView(TemplateView):
    def show_notice(self, notice):
        self.template_name = 'notice.html'
        context = {
            'notice': notice,
        }
        return context


class ProfileView(SharedTemplateView):
    def get(self, request, code):
        # check code validity
        try:
            openid = redis.get('profile:%s' % code)
            if not openid:
                context = self.show_notice(u'链接无效，请重新申请')
                return self.render_to_response(context)
            else:
                mingpian = Mingpian.objects.get(openid=openid)
                form_data = {
                    'name': mingpian.name,
                    'email': mingpian.email,
                    'weixin': mingpian.weixin,
                    'phone_number': mingpian.phone_number,
                    'phone_number_2': mingpian.phone_number_2,
                    'address': mingpian.address,
                    'remark': mingpian.remark,
                }
                form = MingpianForm(form_data)
                context = {
                    'form': form,
                    'openid': mingpian.openid,
                    'is_valid': mingpian.validity,
                    'code': code,
                }
                self.template_name = 'profile.html'
                return self.render_to_response(context)
        except Mingpian.DoesNotExist:
            context = self.show_notice(u'链接无效，请重新申请')
            return self.render_to_response(context)

    def post(self, request, code):
        openid = request.POST['openid']
        try:
            _openid = redis.get('profile:%s' % code)
            if _openid != openid or (not _openid):
                context = self.show_notice(u'无效请求，请重新试一下‍')
                return self.render_to_response(context)

            mingpian = Mingpian.objects.get(openid=openid)
            form = MingpianForm(request.POST)
            if form.is_valid():
                new_data = form.cleaned_data
                if mingpian.validity:
                    # 确保通过审核的用户不可以修改名字
                    new_data['name'] = mingpian.name
                for k, v in new_data.items():
                    mingpian.__setattr__(k, v)
                mingpian.save()
                context = self.show_notice(u'发射成功')
                return self.render_to_response(context)
            else:
                context = {
                    'form': form,
                    'openid': openid,
                    'is_valid': mingpian.validity,
                    'code': code,
                }
                self.template_name = 'profile.html'
                return self.render_to_response(context)
        except Mingpian.DoesNotExist:
            context = self.show_notice(u'非法操作‍')
            return self.render_to_response(context)


class MultiSearchView(SharedTemplateView):
    def get(self, request, code):
        keyword = redis.get('search:%s' % code)
        if keyword == '' or keyword:
            search_result = Mingpian.objects.filter(name__contains=keyword, validity=True).order_by('-name')
            self.template_name = 'multisearch.html'
            context = {
                'keyword': keyword,
                'search_result': search_result,
            }
            return self.render_to_response(context)
        else:
            context = self.show_notice(u'链接无效,请重新申请')
            return self.render_to_response(context)


class DashboardView(SharedTemplateView):
    template_name = 'scepter.html'

    def post(self, request):
        scepter = request.POST['scepter']
        if scepter == settings.MY_SCEPTER:
            self.template_name = 'dashboard.html'
            invaild_mingpian_list = Mingpian.objects.filter(validity=0)
            context = {
                'invaild_mingpian_list': invaild_mingpian_list,
                'scepter': scepter,
            }
            return self.render_to_response(context)
        else:
            context = self.show_notice(u'劣质的权杖')
            return self.render_to_response(context)


@csrf_exempt
def transfer_valid(request):
    if request.method == 'POST':
        scepter = request.POST['scepter']
        if scepter == settings.MY_SCEPTER:
            mingpian_id = request.POST['id']
            mingpian = Mingpian.objects.get(pk=mingpian_id)
            if mingpian.name:
                mingpian.validity = True
                mingpian.save()
                if mingpian.email:
                    send_mail(u'名片儿-通知', u'您已通过名片儿审核', 'zhanga005@nenu.edu.cn', [mingpian.email, ])
                return HttpResponse('ok')
            else:
                return HttpResponse('Name None')
        else:
            return HttpResponse('nu')
    else:
        return HttpResponse('nu2')
