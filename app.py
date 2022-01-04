from flask import Flask
from flask import render_template, jsonify, request
import requests
import json
import platform
from create_log import logger

app = Flask(__name__)
"""
REST channel  使用POST方法访问下面的url
http://<host>:<port>/webhooks/rest/webhook,
参数格式为:
{
  "sender": "test_user",  // sender ID of the user sending the message
  "message": "Hi there!"
}

The response from Rasa Open Source will be a JSON body of bot responses,
for example:
[
  {"text": "Hey Rasa!"}, {"image": "http://example.com/image.jpg"}
]

"""


@app.route('/')
def hello_world():
    """
    Sample hello world
    """
    return render_template('home.html')


def requestRasabotServer(userid, content):
    """
        访问rasa服务
    :param userid: 用户id
    :param content: 自然语言文本
    :return:  json格式响应数据
    """
    params = {'sender': userid, 'message': content}

    if platform.system().lower() == 'windows':
        botIp = "127.0.0.1"
    elif platform.system().lower() == 'linux':
        botIp = "rasa_ep"  # 使用docker-compose中设置的container_name

    botPort = '5005'
    logger.debug(F'server ip {botIp}:{botPort}')
    # rasa使用rest channel
    # https://rasa.com/docs/rasa/user-guide/connectors/your-own-website/#rest-channels
    # POST http://<host>:<port>/webhooks/rest/webhook
    rasaUrl = "http://{0}:{1}/webhooks/rest/webhook".format(botIp, botPort)

    reponse = requests.post(
        rasaUrl,
        data=json.dumps(params),
        headers={'Content-Type': 'application/json'}
    )
    return reponse


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    """
    chat end point that performs NLU using rasa.ai
    and constructs response from response.py
    """
    content = request.form["text"]
    logger.info(F'get from web ui text: {content}')
    if content is None:
        return jsonify({"status": "success", "response": "您输入的内容为空"})
    try:
        response = requestRasabotServer('josiah', content)
        # string
        response = response.text.encode('utf-8').decode("unicode-escape")
        logger.debug(F'retrun from rasa string: {response}')
        response = json.loads(response, strict=False)
        logger.debug(F'retrun from rasa json: {response}')
        res = []
        for text in response:
            res.append(text['text'])

        res = '\n'.join(res)  # 使用回车拼接多个信息
        logger.info(F'retrun from rasa text: {res}')
        return jsonify({"status": "success", "response": res})
    except Exception as e:
        logger.error(e)
        return jsonify({"status": "success", "response": "非常抱歉，连接服务器失败"})


app.config["DEBUG"] = True
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
