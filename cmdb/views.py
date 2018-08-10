from django.http import request, HttpResponse
from django.shortcuts import render
from django.template import loader
from . import  models



# Create your models here.
def index(request):
    #return HttpResponse("你好阿，这是个测试页面")
    return render(request, 'cmdb/index.html')


def index(request):
    aa = models.Asset.objects.all()
    template = loader.get_template('cmdb/index.html')
    context = {
    'Asset': aa,
    }
    return HttpResponse(template.render(context, request))
