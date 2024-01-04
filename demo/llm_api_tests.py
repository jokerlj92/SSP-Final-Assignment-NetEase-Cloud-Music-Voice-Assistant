import requests

import requests
import json
from ttskit import sdk_api
import difflib
import re
from phkit.chinese import symbol_chinese as symbols

import pyttsx3 #相似性对比
import openai
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import os
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential
)
os.environ['OPENAI_API_BASE'] = "https://api.chatanywhere.com.cn/v1"
openai.api_key = "sk-6SSCp1yTRE9kJibtQ6XIkWV3gS39fkfLazaDyoN38x9AFe0f"
openai.api_base = "https://api.chatanywhere.com.cn/v1"
def ask_text(value):
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {"role": "system", "content": "请返回我具体要查询的对象，只输出一个名词即可,并且用我提问中的原词中的一个名词回答，并且不要有过多的解释，也不需要完整的句子.请只输出人名：例如：'查询李荣浩',不要直接输出‘这个句子中的歌手是李荣浩。’或者‘李荣浩。’，直接输出‘李荣浩’；查询新歌，请输出‘新歌’；例如查询晴天，请返回’晴天‘;例如查询和模特相关的歌曲，请返回’模特‘；；"
                                          },
            {
                "role": "user",
                "content": f"请帮我查询 '{value}'",
            },
        ],
        max_tokens=1024,
        temperature=0
    )
    return response.choices[0]['message']['content'].strip()


def string_sim(str1,str2):
    return difflib.SequenceMatcher(None,str1,str2).quick_ratio()
#url = "http://127.0.0.1:8000/api/search?value=李荣浩"

#url_song = "http://127.0.0.1:8000/api/song/lyric?id=27731176"

def get_lyric(url_song):
    try:
        # 发送 GET 请求
        response = requests.get(url_song)
        # 检查请求是否成功
        response.raise_for_status()

        # 解析返回的 JSON 数据
        json_data = response.json()

        #
        # for item in json_data['lrc']:
        #     # 处理每个对象，这里简单地打印出来
        #
        #     print(item)
        print(json_data['lrc']['lyric'])
        str = json_data['lrc']['lyric']
        return str

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
def get_singer(url):
    try:

        # 发送 GET 请求
        response = requests.get(url)
        # 检查请求是否成功
        response.raise_for_status()

        # 解析返回的 JSON 数据
        json_data = response.json()

        print(json_data['artist']['briefDesc'])
            # 处理每个对象，这里简单地打印出来
        str = json_data['artist']['briefDesc']
        return str
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
def get_id(name):
    try:
        url = "http://127.0.0.1:8000/api/search?value="+name
        # 发送 GET 请求
        response = requests.get(url)
        # 检查请求是否成功
        response.raise_for_status()

        # 解析返回的 JSON 数据
        json_data = response.json()

        # 处理 json_data，根据具体结构提取信息

        # 示例：打印整个 JSON 数据
        # print(json_data['result']['songs'])
        # 查询歌手歌曲
        id =0
        for item in json_data['result']['songs']:
            # 处理每个对象，这里简单地打印出来
            #print(item)
            #if str(item['name'])== name:
            if string_sim(str(item['name']),name)>0.8:
                #print("yes")
                #print((item['name'])+name)
                id = item['id']
                #print(item['id'])
                break
        #print(id)
        if(id ==0):
            for item in json_data['result']['songs']:
                #if str(item['artists'][0]['name']) == name:
                if string_sim(str(item['artists'][0]['name']), name) > 0.4:
                    #print(str(item['artists'][0]['name']) + name)
                    #print("yes")
                    id = item['artists'][0]['id']
        #print(id)
        #print(item['name'])

        return id
        # for item in json_data['list']['artists']:
        #     # 处理每个对象，这里简单地打印出来
        #
        #     print(item['name'])

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
def get_hotsinger(url_hot):
    try:
        # 发送 GET 请求
        response = requests.get(url_hot)
        # 检查请求是否成功
        response.raise_for_status()

        # 解析返回的 JSON 数据
        json_data = response.json()

        # 处理 json_data，根据具体结构提取信息
        num = 0
        msg =""
        for item in json_data['list']['artists']:
            # 处理每个对象，这里简单地打印出来
            num+=1
            if(num>=10):
                break
            #print(item['name'])
            msg = msg + str(item['name']) + ','
        print(msg)
            

        return msg
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


def get_simsong(url_songsim):
    try:
        # 发送 GET 请求
        response = requests.get(url_songsim)
        # 检查请求是否成功
        response.raise_for_status()

        # 解析返回的 JSON 数据
        json_data = response.json()

        # 处理 json_data，根据具体结构提取信息
        num = 0
        msg = ''
        for item in json_data['songs']:
            # 处理每个对象，这里简单地打印出来
            num += 1
            if (num >= 10):
                break
            #print(item['name'])
            msg = msg + item['name'] + ','
        print(msg)

        return msg
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
def get_album(url_album):
    try:
        # 发送 GET 请求
        response = requests.get(url_album)
        # 检查请求是否成功
        response.raise_for_status()

        # 解析返回的 JSON 数据
        json_data = response.json()

        # 处理 json_data，根据具体结构提取信息
        num = 0
        msg = ''
        for item in json_data['albums']:
            # 处理每个对象，这里简单地打印出来
            num += 1
            if (num >= 10):
                break
            #print(item['name'])
            #print(item['artist']['name'])
            msg = msg + str(item['artist']['name'])+'的'+str(item['name'] )+ ','

        print(msg)

        return msg
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
def get_newsong(url_new):
    try:
        # 发送 GET 请求
        response = requests.get(url_new)
        # 检查请求是否成功
        response.raise_for_status()

        # 解析返回的 JSON 数据
        json_data = response.json()

        # 处理 json_data，根据具体结构提取信息
        num = 0
        msg = ""
        for item in json_data['result']:

            #print(item['song']['name'])
            msg =msg + item['song']['name']+','
        print(msg)
        return msg
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


def say(txt):
    engine = pyttsx3.init()  # 初始化语音引擎
    engine.setProperty('rate', 200)   #设置语速
    engine.setProperty('volume',2)  #设置音量
    voices = engine.getProperty('voices')
    engine.setProperty('voice',voices[0].id)   #设置第一个语音合成器
    engine.say(txt)
    engine.runAndWait()
    engine.stop()
# 示例用法

# 修改成自己的api key和secret key
API_KEY = "ZyH99kFnafcRyGG5F83fAPd6"
SECRET_KEY = "qhqq9f7bImdksfjVGqf0dF9wYvxMDS41"


def get_answer(s):
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/eb-instant?access_token=" + get_access_token()
    while (1):
        #s = input()
        # 注意message必须是奇数条
        payload = json.dumps({
            "messages": [
                {
                    "role": "user",
                    "content": "请返回我具体要查询的对象，只输出一个名词即可,并且用我提问中的原词中的一个名词回答，并且不要有过多的解释，也不需要完整的句子.现在我的输入是"+s
                }
            ]
        })
        headers = {
            'Content-Type': 'application/json'
        }

        res = requests.request("POST", url, headers=headers, data=payload).json()
        return(res['result'])
def get_answer2(s):
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/eb-instant?access_token=" + get_access_token()
    while (1):
        #s = input()
        # 注意message必须是奇数条
        payload = json.dumps({
            "messages": [
                {
                    "role": "user",
                    "content": "请帮我润色下面词句。"+s
                }
            ]
        })
        headers = {
            'Content-Type': 'application/json'
        }

        res = requests.request("POST", url, headers=headers, data=payload).json()
        return(res['result'])
def get_state(value):
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {"role": "system",
             "content": '现在一共有六个类别，分别是：查询歌手信息、查询歌曲歌词、查询最新专辑、查询新歌、查询相似歌曲、查询歌手排行榜，对应数字1，2，3，4，5，6. 你需要判断输入句子中的信息，并输出对应类别。以下是一些例子：‘查询歌手陶喆’，你只需要输出‘1’，不需要其他额外信息；‘查询模特歌词’，只需要回答‘2’，不需要其他信息回答；‘歌手热度排行榜‘对应数字’6’，只需回答一共阿拉伯数字。注意新专辑和新歌曲不一样。'},
            {
                "role": "user",
                "content": f"请对如下句子种包含的信息进行过分类'{value}'",
            },
        ],
        max_tokens=1024,
        temperature=0
    )
    return response.choices[0]['message']['content'].strip()

def runse(value):
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {"role": "system",
             "content": '请帮我额润色下面句子，使其更通顺，并且限制在50字以内'},
            {
                "role": "user",
                "content": f"'{value}'",
            },
        ],
        max_tokens=1024,
        temperature=0
    )
    return response.choices[0]['message']['content'].strip()

def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))

def remove_non_chinese(sentence):
    # 使用正则表达式删除非中文字符、逗号和句号以外的符号
    cleaned_sentence = re.sub(r'[^\u4e00-\u9fa5\dA-Za-z，、]', '', sentence)
    cleaned_sentence = cleaned_sentence.replace('。', '，')
    return cleaned_sentence
import string

def remove_punctuation(input_string):
    # 使用字符串的 translate 方法和 string.punctuation 来去除标点符号
    chinese_punctuation_pattern = re.compile("[^\u4e00-\u9fa5^a-z^A-Z^0-9]")
    result = chinese_punctuation_pattern.sub('', input_string)

    return result

# 示例用法


def count_and_extract(input_text):
    # 使用正则表达式匹配包含汉字和数字的字符串
    matches = re.findall(r'[\u4e00-\u9fa5\d]+', input_text)

    # 统计数字出现次数
    digit_counts = {}
    for match in matches:
        for char in match:
            if char.isdigit():
                digit_counts[char] = digit_counts.get(char, 0) + 1

    # 找到出现次数最高的数字
    if digit_counts:
        max_digit = max(digit_counts, key=digit_counts.get)
        max_count = digit_counts[max_digit]
        return max_digit
    else:
        return None

#一共6个功能，分别为查询歌手信息、查询歌曲歌词、查询最新专辑、查询新歌、查询相似歌曲、查询歌手排行榜，
#可以输入：查询周杰伦的信息/查询周杰伦
#查询模特歌词
#查询最新专辑
#查询和李白相似的歌曲
#查询排行榜
def get_output(ask):

# if __name__ == '__main__':
    # ask = "现在请你帮我查询歌手排行榜"
    # ask = "查询排行榜"
    state = get_state(ask)
    print(state)
    state = count_and_extract(state)
    print(state)
    key = ask_text(ask)
    id = get_id(key)
    print(key)
    print(id)
    key = remove_punctuation(key)
    state = int(state)
    txt=""
    if(state==1):#查询歌手
        url_singer = "http://127.0.0.1:8000/api/artists/song?id=" + str(id)
        txt = get_singer(url_singer)
        txt = runse(txt)
    if(state==2):#查询歌词
        url_song = "http://127.0.0.1:8000/api/song/lyric?id=" + str(id)
        txt = get_lyric(url_song)
        txt = re.sub(r'\[[^\]]*\]', '', txt)
    if(state==3):#查询新专辑
        url_album = 'http://127.0.0.1:8000/api/artists/album/new'
        txt=get_album(url_album)
        txt = runse("最新的专辑有"+txt)
    if(state==4):#查询新歌
        url_newsong = "http://127.0.0.1:8000/api/song/newsong"
        txt = get_newsong(url_newsong)
        txt = runse("最新的歌曲有" + txt)
    if (state==5):#查询相似歌曲
        url_songsim = 'http://127.0.0.1:8000/api/song/simi?id=' + str(id)
        txt = get_simsong(url_songsim)
        txt = runse("相似的歌曲有" + txt)
    if(state==6):#查询歌手热度排行
        url = url_hot = "http://127.0.0.1:8000/api/artists/toplist"
        txt = get_hotsinger(url)
        txt = runse("现在的歌手热度排行依次为：" + txt)
    print(txt)
    say(txt)
    return txt
