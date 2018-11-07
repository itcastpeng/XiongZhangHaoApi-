from django.test import TestCase

# Create your tests here.



wenzhang = """ 
17 诊疗科目(封面频道) 0
18 ─痔疮疾病 1
22 ──内痔 2
23 ──外痔 2
24 ──混合痔 2
25 ──痔疮 2
19 ─肛门损伤 1
26 ──脱肛 2
27 ──肛瘘 2
28 ──肛裂 2
29 ──大便出血 2
20 ─肠道疾病 1
40 ──结肠炎 2
41 ──直肠炎 2
42 ──肠炎 2
43 ──肠息肉 2
21 ─女子肛肠 1
88 ─权威技术 1
55 ─肛周疾病 1
32 ──肛周脓肿 2
33 ──肛门湿疹 2
34 ──肛门异物 2
35 ──肛门瘙痒 2
56 ─排泄疾病 1
36 ──便秘 2
37 ──腹泻 2
39 ──大便异常 2
45 患者中心(封面频道) 0
46 ─位置交通 1
47 ─就医流程 1
48 ─常见问题 1
49 ─24小时免费咨询热线 1
57 ─病人权利义务 1
58 ─出入院注意 1
59 ─就诊误区 1
61 ─医保指南 1
89 公益事业 0
62 特色服务(封面频道) 0
63 ─夜门诊 1
64 ─私密诊室 1
65 ─特色导诊 1
66 ─0等候服务 1
67 ─男女分诊 1
70 ─VIP病房 1
71 ─健康管理中心 1
72 了解川肛(封面频道) 0
1 ─川肛简介 1
16 ─诊疗设备 1
80 ─对外交流 1
79 ─学术成果 1
78 ─楼层分布 1
77 ─诊疗环境 1
76 ─远景规划 1
75 ─院长寄语 1
74 ─川肛院训 1
73 ─川肛荣誉 1
81 ─员工工会 1
92 医技科室 0
93 ─超声科 1
94 ─病理科 1
95 ─检验科 1
96 ─放射科 1
97 ─医学部 1
98 ─核医学科 1
99 ─病案统计科 1
100 ─营养科 1

"""
# data_list = []
# for wen in wenzhang.split('\n'):
#     if wen.strip():
#         class_id = wen.split(' ')[2]
#         class_name = wen.split(' ')[1]
#         level = class_name.count('--')
#
#         if len(data_list) - 1 >= level:
#             data_list[level] = class_id
#         else:
#             data_list.append(class_id)
#
#         parent_data = {}
#         if level == 0:
#             print(class_id, class_name)
#         else:
#             print(class_id, class_name, data_list[level -1])
        # parent_data[class_id] = {
        #     'class_name':class_name,
        #     'children':{}
        # }
        #
        # print('v-data_list------->', data_list)



cookie_data = 'BAIDUID=7209E6BE5B5689600FE80DE10A797DD8:FG=1;BDUSS=lLVGdXLVJhRzkxMHdHcVNEUWZJRVV-WnN5VTVEUVdGRER5SkY3bjk3eGNnWVphQVFBQUFBJCQAAAAAAAAAAAEAAADiEgLOwLTEoG63odrEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFz0Xlpc9F5aWF;PTOKEN=41275f1ce69be19d1c8074c1e5488dc8;STOKEN=7153c8aaed2e53282a76e6f1f28a8b847442fdfcd38c4a850fee7e058e3f913a'

cookie_dict = {}
for i in cookie_data.split(';'):
    # print(i)
    k, v = i.split('=', maxsplit=1)
    # print(k, v )
    cookie_dict[k] = v

print(cookie_dict)


