from openai import OpenAI
import json
from flask import Flask, jsonify,request
from flask_cors import CORS

# 填你的秘钥
# openai.api_key = "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"
client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key= "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",
)

# chat_completion = client.chat.completions.create(
#     messages=[
#         {
#             "role": "user",
#             "content": "Say this is a test",
#         }
#     ],
#     model="gpt-3.5-turbo",
# )
# 提问代码
messages=[]
def chat_gpt(prompt):
    # 你的问题
    prompt = prompt
    
    # 调用 ChatGPT 接口
    completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Say this is a test",
            }
        ],
        model="gpt-3.5-turbo",
    )
    response = completion.choices[0].message

    return response



app = Flask(__name__)
CORS(app)

@app.route('/api', methods=['GET'])
def getAnswer():
    messageinfo = request.args.get('messageinfo', default=1, type=str)
    print(messageinfo)
    res = chat_gpt(messageinfo)
    return jsonify({"answer":res})

if __name__ == '__main__':
    app.run()

# chat_gpt("使用python 写一个https接口 ，在web端可以使用fetch方式调用，使用英文回答")

