import os
import openai
import json

# 填你的秘钥
openai.api_key = "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"

# 提问代码
def chat_gpt(prompt):
    # 你的问题
    prompt = prompt
    
    # 调用 ChatGPT 接口
    model_engine = "text-davinci-003"
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    response = completion.choices[0].text
    return response

from flask import Flask, jsonify,request
import random
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api', methods=['GET'])
def getAnswer():
    # messageinfo = json.loads(request.args.get('data'))
    messageinfo = request.args.get('messageinfo', default=1, type=str)
    print(messageinfo)
    res = chat_gpt(messageinfo)
    return jsonify({"answer":res})

if __name__ == '__main__':
    app.run()

# chat_gpt("使用python 写一个https接口 ，在web端可以使用fetch方式调用，使用英文回答")

