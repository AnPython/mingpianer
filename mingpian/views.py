# coding: utf-8

from django.utils import timezone
from django.conf import settings
from django.shortcuts import HttpResponse
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt


from .models import Mingpian, Philosopherstone
from .forms import MingpianForm


class ProfileView(TemplateView):
    def get(self, request, code):
        # check code validity
        try:
            stone = Philosopherstone.objects.get(code=code)
            create_datetime = stone.create_datetime
            current_datetime = timezone.now()
            timedelta_seconds = (current_datetime-create_datetime).seconds
            if timedelta_seconds > 600:
                stone.delete()
                context = self.show_notice(u'链接已过期，请重新申请')
                return self.render_to_response(context)
            else:
                mingpian = stone.player
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
        except Philosopherstone.DoesNotExist:
            context = self.show_notice(u'无效链接，请重新申请')
            return self.render_to_response(context)

    def post(self, request, code):
        openid = request.POST['openid']
        try:
            stone = Philosopherstone.objects.get(player__openid=openid, code=code)
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
                stone.delete()
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
        except (Philosopherstone.DoesNotExist, Mingpian.DoesNotExist):
            context = self.show_notice(u'非法操作‍')
            return self.render_to_response(context)

    def show_notice(self, notice):
        self.template_name = 'notice.html'
        context = {
            'notice': notice,
        }
        return context


class DashboardView(TemplateView):
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
            self.template_name = 'notice.html'
            context = {
                'notice': u'地狱权杖',
            }
            return self.render_to_response(context)


@csrf_exempt
def transfer_valid(request):
    if request.method == 'POST':
        scepter = request.POST['scepter']
        if scepter == settings.MY_SCEPTER:
            mingpian_id = request.POST['id']
            mingpian = Mingpian.objects.get(pk=mingpian_id)
            mingpian.validity = True
            mingpian.save()
            return HttpResponse('ok')
        else:
            return HttpResponse('nu')
    else:
        return HttpResponse('nu2')
