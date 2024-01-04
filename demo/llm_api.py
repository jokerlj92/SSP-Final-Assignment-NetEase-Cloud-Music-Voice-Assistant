import requests
import json
from ttskit import sdk_api
import difflib
import re
from phkit.chinese import symbol_chinese as symbols
import pyttsx3

def string_sim(str1, str2):
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
            if string_sim(str(item['name']),name)>0.5:
                #print("yes")
                id = item['id']
                break
                print(item['id'])
        #print(id)
        if(id ==0):
            for item in json_data['result']['songs']:
                #if str(item['artists'][0]['name']) == name:
                if string_sim(str(item['artists'][0]['name']), name) > 0.4:
                    #print("yes")
                    id = item['artists'][0]['id']
        print(id)
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
        for item in json_data['list']['artists']:
            # 处理每个对象，这里简单地打印出来

            print(item['name'])

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


def get_ans_singer(input_sentence):
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/eb-instant?access_token=" + get_access_token()
    while (1):
        #s = input()
        # 注意message必须是奇数条
        payload = json.dumps({
            "messages": [
                {
                    "role": "user",
                    "content": f"你只需要识别这个句子中的歌手：{input_sentence}, 例如：不要输出‘这个句子中的歌手是李荣浩。‘，或者‘李荣浩。’，直接输出：’李荣浩’。不要输出’这个句子中的歌手是林俊杰。‘，直接输出’林俊杰‘。没有识别到歌手请输出固定内容：‘没有识别到歌手’，不要输出其他汉字，也不要输出任何标点符号。"
                    # "content": "请返回我具体要查询的对象，只输出一个名词即可,用我提问中的原词回答，现在我的输入是" + input_sentence
                }
            ]
        })
        headers = {
            'Content-Type': 'application/json'
        }
        res = requests.request("POST", url, headers=headers, data=payload).json()
        return(res['result'])

def get_ans_song(input_sentence):
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/eb-instant?access_token=" + get_access_token()
    while (1):
        #s = input()
        # 注意message必须是奇数条
        payload = json.dumps({
            "messages": [
                {
                    "role": "user",
                    "content": f"你只需要识别这个句子中的歌曲：{input_sentence}, 请只输出歌曲名称'xxx'；没有识别到歌曲请输出固定内容：‘没有识别到歌曲’，不要输出其他汉字，也不要输出任何标点符号。"
                    # "content": "请返回我具体要查询的对象，只输出一个名词即可,用我提问中的原词回答，现在我的输入是" + input_sentence
                }
            ]
        })
        headers = {
            'Content-Type': 'application/json'
        }
        res = requests.request("POST", url, headers=headers, data=payload).json()
        return(res['result'])

def get_answer(s):
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/eb-instant?access_token=" + get_access_token()
    while (1):
        #s = input()
        # 注意message必须是奇数条
        payload = json.dumps({
            "messages": [
                {
                    "role": "user",
                    "content": f"请对下文进行概述，使其完整通顺并且符合人的对话特性，一定要限制在50字以内：{s}"
                }
            ]
        })
        headers = {
            'Content-Type': 'application/json'
        }

        res = requests.request("POST", url, headers=headers, data=payload).json()
        return(res['result'])

def get_state(entity):
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/eb-instant?access_token=" + get_access_token()
    while (1):
        #s = input()
        # 注意message必须是奇数条
        payload = json.dumps({
            "messages": [
                {
                    "role": "user",
                    "content": "请判断" + entity
                    # "content": "请说明，输入是歌手名字，还是歌曲名字，还是其他：请回答1，2，3中的一个数字，对应上述情况" + entity
                }
            ]
        })
        headers = {
            'Content-Type': 'application/json'
        }

        res = requests.request("POST", url, headers=headers, data=payload).json()
        return(res['result'])

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

def get_output(transcription):
    singer = get_ans_singer(transcription)
    song = get_ans_song(transcription)
    # state = get_state(key)
    # state=2
    print('singer识别结果：', singer)
    print('song识别结果：', song)

    url_singer = 0
    url_song = 0

    if singer != '没有识别到歌手':
        url_singer = "http://127.0.0.1:8000/api/artists/song?id=" + str(get_id(singer))
    if song != '没有识别到歌曲':
        url_song = "http://127.0.0.1:8000/api/song/lyric?id="+str(get_id(song[5:]))

    print(url_singer)
    print(url_song)

    #txt =get_singer(url_singer)
    global txt

    if (url_singer):
        #url_singer = "http://127.0.0.1:8000/api/artists/song?id="+str(id)
        # url_hot = "http://127.0.0.1:8000/api/artists/toplist"
        # txt = get_hotsinger(url_hot)
        txt = get_singer(url_singer)
        txt = get_answer(txt)
    elif(url_song):
        #url_song = "http://127.0.0.1:8000/api/song/lyric?id=" + str(id)
        txt = get_lyric(url_song)
        txt = re.sub(r'\[[^\]]*\]', '', txt)
    else:
        txt = '抱歉我没有识别到任何歌手和歌曲'

    say(txt)
    return txt
# "content": "我的询问包含三种情况，你需要甄别我的输入是哪种情况。第一种情况，我的输入包含歌手名，1.第二种情况，我的输入包含歌曲名字，你需要回答2.第三种情况，我的输入是歌手热度排行，你需要回答3.请不要有其他的输出，不需要解释答案原因，直接给出答案即可，如果仅有歌手名，那么属于情况1，如果既有歌手名又有歌曲名属于情况2。你只需要给出一个阿拉伯数字1-3中的一个现在我的输入是："+s
