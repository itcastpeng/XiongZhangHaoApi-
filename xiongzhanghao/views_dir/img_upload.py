import json,time,os
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from xiongzhanghao.publicFunc import UEditorUploadConfig


# 图片上传
@csrf_exempt
def image_upload(request):
    # 获取配置信息
    if request.GET.get('action') == 'config':
        '''
        为uploadimage 上传图片 对图片进行处理
        config.json 配置文件 详细设置参考：http://fex.baidu.com/ueditor/#server-deploy
        '''
        if "callback" not in request.GET:
            return JsonResponse(UEditorUploadConfig.UEditorUploadSettings)
        else:
            return_str = "{0}({1})".format(request.GET["callback"], json.dumps(UEditorUploadConfig.UEditorUploadSettings, ensure_ascii=False))
            print('return_str -->', return_str)
            return HttpResponse(return_str)

    # 上传图片
    elif request.GET.get('action') == 'uploadimage':
        img = request.FILES.get('upfile')
        name = request.FILES.get('upfile').name

        print('------request.FILES-------->>',request.FILES.get,img,name)

        allow_suffix = ['jpg', 'png', 'jpeg', 'gif', 'bmp']
        # file_suffix = name.split(".")[-1]
        file_suffix = name.split(".")[-1]

        if file_suffix not in allow_suffix:
            return {"state": 'error', "name": name, "url": "", "size": "", "type": file_suffix}

        # 上传文件路径
        dir_name = os.path.join('statics', 'img')

        file_name = str(int(time.time() * 1000)) + "." + file_suffix

        filenameurl = os.path.join(dir_name, file_name)
        print('filenameurl -->', filenameurl)
        with open(filenameurl, 'wb+') as destination:
            for chunk in img.chunks():
                destination.write(chunk)

        data = {"state": 'SUCCESS', "url": '/' + filenameurl, "title": file_name, "original": name, "type": file_suffix}

        print('-------data-------->>',data)

        return JsonResponse(data)


    else:
        return HttpResponse('请求错误')