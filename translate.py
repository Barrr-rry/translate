# encoding:utf-8
import requests
import json
import execjs
import pymysql
import logging
import time
from urllib import parse
from Similarity import similarity
from datetime import datetime
from tqdm import tqdm, trange


class Py4Js:

    def __init__(self):
        self.ctx = execjs.compile(""" 
        function TL(a) { 
        var k = ""; 
        var b = 406644; 
        var b1 = 3293161072; 

        var jd = "."; 
        var $b = "+-a^+6"; 
        var Zb = "+-3^+b+-f"; 

        for (var e = [], f = 0, g = 0; g < a.length; g++) { 
            var m = a.charCodeAt(g); 
            128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023), 
            e[f++] = m >> 18 | 240, 
            e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224, 
            e[f++] = m >> 6 & 63 | 128), 
            e[f++] = m & 63 | 128) 
        } 
        a = b; 
        for (f = 0; f < e.length; f++) a += e[f], 
        a = RL(a, $b); 
        a = RL(a, Zb); 
        a ^= b1 || 0; 
        0 > a && (a = (a & 2147483647) + 2147483648); 
        a %= 1E6; 
        return a.toString() + jd + (a ^ b) 
    }; 

    function RL(a, b) { 
        var t = "a"; 
        var Yb = "+"; 
        for (var c = 0; c < b.length - 2; c += 3) { 
            var d = b.charAt(c + 2), 
            d = d >= t ? d.charCodeAt(0) - 87 : Number(d), 
            d = b.charAt(c + 1) == Yb ? a >>> d: a << d; 
            a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d 
        } 
        return a 
    } 
    """)

    def get_tk(self, text):
        return self.ctx.call("TL", text)


class Translate(object):
    def __init__(self, to_language='zh-TW', this_language='en', read=False, token='Btu6BYZCU4bWRw45LS6f3W1nrNm0FRYVk3BkMqsxcnq'):
        self.this_language = this_language
        self.to_language = to_language
        self.read = read
        self.js = Py4Js()
        self.token = token

    def open_url(self, url):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
        # req = requests.get(url=url, headers=headers, timeout=8)
        try:
            req = requests.get(url=url, headers=headers)
        except Exception as e:
            logging.error(e)
            lineNotifyMessage(e, self.token)
        return req

    def build_url(self, text, tk):
        baseUrl = 'http://translate.google.cn/translate_a/single'
        baseUrl += '?client=webapp&'
        baseUrl += 'sl=%s&' % self.this_language
        baseUrl += 'tl=%s&' % self.to_language
        baseUrl += 'hl=zh-CN&'
        baseUrl += 'dt=at&'
        baseUrl += 'dt=bd&'
        baseUrl += 'dt=ex&'
        baseUrl += 'dt=ld&'
        baseUrl += 'dt=md&'
        baseUrl += 'dt=qca&'
        baseUrl += 'dt=rw&'
        baseUrl += 'dt=rm&'
        baseUrl += 'dt=ss&'
        baseUrl += 'dt=t&'
        baseUrl += 'ie=UTF-8&'
        baseUrl += 'oe=UTF-8&'
        baseUrl += 'clearbtn=1&'
        baseUrl += 'otf=1&'
        baseUrl += 'pc=1&'
        baseUrl += 'srcrom=0&'
        baseUrl += 'ssel=0&'
        baseUrl += 'tsel=0&'
        baseUrl += 'kc=2&'
        baseUrl += 'tk=' + str(tk) + '&'
        baseUrl += 'q=' + parse.quote(text)
        return baseUrl

    def translate(self, text):
        tk = self.js.get_tk(text)
        if len(text) > 4891:
            raise Exception("超過翻譯長度限制")
        url = self.build_url(text, tk)
        data = self.open_url(url).content.decode('utf-8')
        tmp = json.loads(data)
        json_array = tmp[0]
        result = None
        for json_item in json_array:
            result = (result + " " + json_item[0] if result else json_item[0]) if json_item[0] else result
        return result


def lineNotifyMessage(msg, token):
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {'message': msg}
    r = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=payload)
    return r.status_code


def connDB():
    db = pymysql.connect(host='163.18.10.123', port=3306,
                         user='EPuser', passwd='e507@mis', db='entries', charset='utf8mb4')
    cur = db.cursor()
    return db, cur


def closeDB():
    db.close()


def crudTable(method, sql):
    try:
        cur.execute(sql)
    except (pymysql.Error, pymysql.Warning) as e:
        return e
    res = lambda method: cur.fetchall() if method == 'read' else True
    db.commit() if method != 'read' else None
    return res(method)


def translate_table(table):
    filter_dct = {
                    '1': ['Btu6BYZCU4bWRw45LS6f3W1nrNm0FRYVk3BkMqsxcnq', 'AND id%2=1 AND id%3!=0 AND id%4!=0 AND id%5!=0 AND id%6!=0'],
                    '2': ['xTix6RnFDWBtOfDATgURmnrvyxIFPmRcGSIleRsGkym', 'AND id%2=0 AND id%3!=0 AND id%4!=0 AND id%5!=0 AND id%6!=0'],
                    '3': ['Nu411JDgWGBfyElBJRboSPBuKnMnae7cp24OKTLhFJe', 'AND id%3=0 AND id%4!=0 AND id%5!=0 AND id%6!=0'],
                    '4': ['YbpLcVThmlMg597qSF94nUTdaJuXeEuz6V7mO0EzjIE', 'AND id%4=0 AND id%5!=0 AND id%6!=0'],
                    '5': ['jOOhY3s6KF5rLVI65flZ7msOxMdNVvwfPmvWXWym75C', 'AND id%5=0 AND id%6!=0'],
                    '6': ['a5sFhBIqbZOYSspwtVTp4fAwFg2lQODXKC9ZWSRDtN1', 'AND id%6=0'],
    }
    print('請輸入批次：')
    num = input()
    token = filter_dct.get(num)[0]
    sql = f'select * from {table} where Translate_Eng IS NULL {filter_dct.get(num)[1]}'
    target = crudTable('read', sql)
    n = 0
    ordinal = lambda n: f'{n}{"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4]}'
    for col in target:
        n += 1
        start_time = time.time()
        eng = col[4]
        chinese = Translate(token=token).translate(eng)
        translate_eng = Translate('en', 'zh-TW', token=token).translate(chinese).replace('\"', '\'')
        sm = similarity(eng, translate_eng)
        update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sql = f'UPDATE {table} SET chinese = \"{chinese}\", Translate_Eng = \"{translate_eng}\", Similarity={sm}, update_time=\"{update_time}\" WHERE id={col[0]};'
        res = crudTable('update', sql)
        end_time = time.time()
        if res:
            print(f'INFO : The {ordinal(n)} data translation was successful.  Process time : {end_time-start_time} sec.')
            lineNotifyMessage(f'INFO:已完成{n}筆資料。', token) if n % 500 == 0 else None
        else:
            logging.error(res)
            lineNotifyMessage(res, token)
            continue
    lineNotifyMessage(f'INFO:本次翻譯已完成，共翻譯了{n}筆資料。', token)


def re_similarity(table):
    target_sql = f'select id, Content, Translate_Eng from {table} where Similarity < 0.5'
    targets = crudTable('read', target_sql)
    for target in tqdm(targets):
        sm = similarity(target[1], target[2])
        update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        update_sql = f'UPDATE {table} SET Similarity={sm}, update_time=\"{update_time}\" WHERE id={target[0]};'
        res = crudTable('update', update_sql)
        # print(f'success, Similarity = {sm}') if res else print(res)


def rm_sameData(table):
    target_sql = f'select id, Content from {table}'
    targets = list(crudTable('read', target_sql))
    for target in tqdm(targets):
        sql = f'select id from {table} where id != {target[0]} and Content = \"{target[1]}\"'
        tmps = crudTable('read', sql)
        if tmps:
            for tmp in tmps:
                delete_sql = f'delete from {table} WHERE id={tmp[0]};'
                res = res = crudTable('delete', delete_sql)
                print(f'success, target_id = {target[0]}, content = {target[1]}') if res else print(res)
                targets.remove((tmp[0], target[1]))


if __name__ == '__main__':
    db, cur = connDB()
    table = 'sent'
    n = 0
    translate_table(table)
    # re_similarity(table)
    # rm_sameData(table)
    closeDB()

