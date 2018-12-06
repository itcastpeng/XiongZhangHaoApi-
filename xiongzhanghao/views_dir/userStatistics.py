from xiongzhanghao import models
from xiongzhanghao.publicFunc import Response
from xiongzhanghao.publicFunc import account
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from xiongzhanghao.publicFunc.condition_com import conditionCom
from xiongzhanghao.forms.add_fans import SelectForm
import json, requests, datetime, time
from openpyxl import Workbook
from openpyxl.styles.alignment import Alignment





# cerf  token验证 用户展示模块
@csrf_exempt
@account.is_token(models.xzh_userprofile)
def userStatistics(request):
    response = Response.ResponseObj()
    forms_obj = SelectForm(request.GET)
    if forms_obj.is_valid():
        now = datetime.datetime.now().strftime('%Y-%m-%d')
        current_page = forms_obj.cleaned_data['current_page']
        length = forms_obj.cleaned_data['length']
        print('forms_obj.cleaned_data -->', forms_obj.cleaned_data)
        order = request.GET.get('order', '-create_date')
        field_dict = {
            'id': '',
            'username': '__contains',
            'create_date': '__contains',
            'belong_user_id': '',
        }
        q = conditionCom(request, field_dict)


        print('q -->', q)
        objs = models.user_statistics.objects.select_related('belong_user').filter(q).order_by(order)
        count = objs.count()

        if length != 0:
            start_line = (current_page - 1) * length
            stop_line = start_line + length
            objs = objs[start_line: stop_line]

        # 返回的数据
        ret_data = []

        for obj in objs:
            #  将查询出来的数据 加入列表
            ret_data.append({
                'id': obj.id,
                'belong_user_id':obj.belong_user_id,    # 归属人ID
                'belong_user':obj.belong_user.username, # 归属人名字

                'public_num':obj.public_num,            # 发布数量
                'fans_num':obj.fans_num,                # 粉丝数量
                'zhishu':obj.zhishu,                    # 指数
                'zhanxianliang':obj.zhanxianliang,      # 展现量
                'dianjiliang':obj.dianjiliang,          # 点击量

                'baidu_shoulu':obj.baidu_shoulu,        # 百度收录数量
                # 'baidu_shoulu_url':obj.baidu_shoulu_url,  # 百度收录链接
                'index_show':obj.index_show,            # 熊掌号主页展示条数 （主页收录）
                # 'index_show_url':obj.index_show_url,  # 熊掌号主页展示url
                'admin_shoulu':obj.admin_shoulu,        # 熊掌号后台收录条数
                # 'admin_shoulu_url':obj.admin_shoulu_url,  # 熊掌号后台收录url
                'create_date':obj.create_date.strftime('%Y-%m-%d'), # 创建时间

            })

        #  查询成功 返回200 状态码
        response.code = 200
        response.msg = '查询成功'
        response.data = {
            'ret_data': ret_data,
            'count':count,
        }

    else:
        response.code = 301
        response.data = json.loads(forms_obj.errors.as_json())

    return JsonResponse(response.__dict__)



#  增删改
#  csrf  token验证
@csrf_exempt
@account.is_token(models.xzh_userprofile)
def userStatistics_oper(request, oper_type, o_id):
    response = Response.ResponseObj()
    user_id = request.GET.get('user_id')
    if request.method == 'POST':
        if oper_type == 'userStatisticsExcle':
            wb = Workbook()
            ws = wb.active
            ws.cell(row=1, column=1, value="客户名称:")
            ws.cell(row=1, column=6, value="生成报表时间:")
            ws.cell(row=2, column=6, value="数据总数:")
            ws.cell(row=3, column=6, value="应加粉总数量:")
            ws.cell(row=4, column=6, value="实加粉总数量:")

            ws.cell(row=4, column=1, value="熊掌号搜索关键词")
            ws.cell(row=4, column=2, value="加粉前")
            ws.cell(row=4, column=3, value="加粉数")
            ws.cell(row=4, column=4, value="加粉后")
            ws.cell(row=4, column=5, value="加粉时间")


            # print('设置列宽')
            ws.column_dimensions['A'].width = 25
            ws.column_dimensions['B'].width = 25
            ws.column_dimensions['C'].width = 25
            ws.column_dimensions['D'].width = 25
            ws.column_dimensions['E'].width = 25
            ws.column_dimensions['F'].width = 25
            ws.column_dimensions['G'].width = 25

            ws['A1'].alignment = Alignment(horizontal='right', vertical='center')
            ws['B1'].alignment = Alignment(horizontal='center', vertical='center')
            ws['C1'].alignment = Alignment(horizontal='center', vertical='center')
            ws['A2'].alignment = Alignment(horizontal='right', vertical='center')
            ws['C2'].alignment = Alignment(horizontal='right', vertical='center')
            ws['E1'].alignment = Alignment(horizontal='right', vertical='center')

            row = 5
            addObjs = models.xzh_add_fans.objects.filter(belong_user_id=o_id).order_by('-create_date')
            add_Objs = models.xzh_add_fans.objects.filter(belong_user_id=o_id).order_by('create_date')
            addObjsCount = addObjs.count()
            if addObjs:
                after_add_fans = addObjs[0].after_add_fans  #最后一次 加粉 数量
                befor_add_fans = add_Objs[0].befor_add_fans # 加粉前数量
                print(after_add_fans, befor_add_fans)
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                ws.cell(row=1, column=2, value="{}".format(addObjs[0].belong_user.username))
                ws.cell(row=1, column=7, value="{}".format(now))
                ws.cell(row=2, column=7, value="{}".format(addObjsCount))
                ws.cell(row=4, column=7, value="{}".format(after_add_fans-befor_add_fans))
                yingjiafen_num = 0
                for addObj in addObjs:
                    yingjiafen_num += addObj.add_fans_num
                    print('addObj.create_date===========================> ',addObj.create_date)
                    ws.cell(row=row, column=1, value="{}".format(addObj.search_keyword))
                    ws.cell(row=row, column=2, value="{}".format(addObj.befor_add_fans))
                    ws.cell(row=row, column=3, value="{}".format(addObj.add_fans_num))
                    ws.cell(row=row, column=4, value="{}".format(addObj.after_add_fans))
                    ws.cell(row=row, column=5, value="{}".format(addObj.create_date))
                    row += 1
                ws.cell(row=3, column=7, value="{}".format(yingjiafen_num))

                # # 合并单元格        开始行      结束行       用哪列          占用哪列
                ws.merge_cells(start_row=1, end_row=2, start_column=1, end_column=1)
                ws.merge_cells(start_row=1, end_row=2, start_column=2, end_column=4)





                timestamp = str(int(time.time())) + str(time.time()).split('.')[1][2:-1]
                xlsx_url = 'statics/fansExcle/{}.xlsx'.format(timestamp)
                # wb.save(xlsx_url)
                wb.save('./5.xlsx')
                return_xlsx_path = 'http://xiongzhanghao.zhugeyingxiao.com:8003/' + xlsx_url
                response.code = 200
                response.msg = '生成完成'
                response.data = return_xlsx_path
            else:
                response.code = 301
                response.msg = '该用户无加粉数据'

    else:
        response.code = 402
        response.msg = '请求错误'
    return JsonResponse(response.__dict__)














