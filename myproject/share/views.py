from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponsePermanentRedirect,HttpResponse
from .models import Upload
import random
import string
import json


class HomeView(View):
    """用来展示主题的类视图"""
    def get(self,request):
        return render(request,"base.html",{})
    def post(self,request):
        if request.FILES:
            file = request.FILES.get('file')
            name = file.name
            size = int(file.size)

            with open('static/file/'+name,'wb') as f:
                f.write(file.read())

            code = ''.join(random.sample(string.digits,8))
            u = Upload(
                path = 'static/file/' + name,
                name = name,
                Filesize = size,
                PCIP= str(request.META['REMOTE_ADDR'])
            )
            u.save()

            return HttpResponsePermanentRedirect('/s/'+code)

class DisplayView(View):
    """展示文件的视图类"""
    def get(self,request,code):
        u = Upload.objects.filter(code=str(code))
        if u:
            for i in u:
                i.DownloadDocount +=1
                i.save()
        return render(request,'content.html',{"content":u})

class MyView(View):
    """定义一个MyView用于完成用户管理功能"""
    def get(self,request):
        #获取用户ip
        IP = request.META['REMOTE_ADDR']
        #查找数据
        u = Upload.objects.filter(PCIP=str(IP))
        for i in u:
            i.DownloadDocount +=1
            i.save()
        return render(request,'content.html',{'content':u})


class SearchView(View):
    def get(self,request):
        #获取get请求的kw 值，即搜索内容
        code = request.GET.get("kw")
        u = Upload.objects.filter(name=str(code))
        data = {}
        if u:
            for i in range(len(u)):
                """将符合条件的数据放在data中"""
                u[i].DownloadDocount += 1
                u[i].save()
                data[i] = {}
                data[i]['download'] = u[i].DownloadDocount
                data[i]['filename'] = u[i].name
                data[i]['id'] = u[i].id
                data[i]['ip'] = u[i].ip
                data[i]['size'] = u[i].Filesize
                data[i]['time'] = str(u[i].Datatime.strftime('%Y-%m-%d %H:%M'))
                #时间格式化
                data[i]['key'] = u[i].code

            return HttpResponse(json.dumps(data),content_type="application/json")



