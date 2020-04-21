from django.http import JsonResponse, HttpResponse
from pearbook import settings
from pearbook.upload import models
import hashlib
import os
import random
import time

# Create your views here.
SUCCESS_CODE = 200
SUCCESS_MESSAGE = "上传成功"

FAILURE_CODE = 100
FAILURE_MESSAGE = "上传失败"
SIZE_ERROR = "文件大小不得多于5M"


type_list = ['.png', '.jpg', '.gif', 'jpeg', '.bmp']


def get_file_md5(file):
    md5_obj = hashlib.md5()
    for chunk in file.chunks():
        md5_obj.update(chunk)
    return md5_obj.hexdigest()


# 重命名并写入
def rename(file):
    times = time.strftime('%Y%m%d%H%M%S')
    ran = random.randint(0, 1000)
    ext = os.path.splitext(file.name)[1]
    new_file = "{}{}{}".format(times, ran, ext)
    path = os.path.join('static/images', new_file).replace('\\', '/')
    read = open(path, 'wb+')
    for chunk in file.chunks():
        read.write(chunk)
    read.close()
    return path


def upload(request):
    if request.method == 'POST':
        base_url = "http://" + request.META["HTTP_HOST"] + "/"
        files = request.FILES
        if files:
            ret = {'code': SUCCESS_CODE, 'message': SUCCESS_MESSAGE, 'urls': []}
            for fileName in files:
                file = request.FILES.get(fileName)
                if file.size > 5 * 1024 * 1024:
                    return JsonResponse({'code': FAILURE_CODE, 'message': SIZE_ERROR})
                md5 = get_file_md5(file)
                img_obj = models.UploadImage.objects.filter(imgMd5=md5)
                if img_obj:
                    url = base_url + img_obj.first().imgPath
                    info = {'name': file.name, 'url': url}
                else:
                    path = rename(file)
                    create = models.UploadImage.objects.create(
                        imgName=os.path.basename(path),
                        imgMd5=md5,
                        imgType=os.path.splitext(file.name)[1],
                        imgSize=file.size,
                        imgPath=path)
                    url = base_url + create.imgPath
                    info = {'name': file.name, 'url': url}
                ret['urls'].append(info)
            return JsonResponse(ret)
        else:
            # return JsonResponse({'code': FAILURE_CODE, 'message': FAILURE_MESSAGE})
            return JsonResponse({'code': 123, 'message': 123})


def upload_file(request):
    if request.method == 'POST':
        # file = request.FILES.get('file')
        file = request.FILES.get('file')
        name = file.name
        # print(file)
        # return HttpResponse(settings.MEDIA_ROOT)
        with open(os.path.join(settings.MEDIA_ROOT,name), 'wb') as fp:
            for chunk in file.chunks():
                fp.write(chunk)
        url = request.build_absolute_uri(settings.MEDIA_URL+name)
        # http://127.0.1:8000/media/abc.jpg
        return HttpResponse(url)


# 注意 测试页面
def test(request):
    if request.method == 'GET':
        return JsonResponse({'code': 212, 'message': 'dfdfd'})