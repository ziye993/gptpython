import pyodbc
from openai import OpenAI
import json
from flask import Flask, jsonify,request,render_template
from flask_cors import CORS
import pprint
from token_utils import generate_token, decode_token

conn = pyodbc.connect('DRIVER={SQL Server};SERVER=ziye993;DATABASE=gptDb;UID=ziye;PWD=zwd112112;Trusted_Connection=yes')
if conn:
    print("连接成功!")
client = OpenAI(
    api_key= "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",
)
def chat_gpt(prompt):
    # 你的问题
    prompt = prompt
    completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content":prompt,
            }
        ],
        model="gpt-3.5-turbo",
    )
    response = completion.choices[0].message.content
    pprint.pprint(response)
    return response

app = Flask(__name__) 
CORS(app)
# 用户登录接口
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # 在实际应用中，这里需要编写登录验证逻辑
    # 检查用户名和密码是否匹配，如果匹配则生成并返回token
    # 否则返回登录失败的消息
    # 这里仅作为示例，不包含实际的身份验证逻辑
    if username == 'example_user' and password == 'example_password':
        token = generate_token(username)
        return jsonify({'token': token})
    else:
        return jsonify({'error': '请检查用户名或密码'})

# 用户注册接口
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    # 在实际应用中，这里需要编写用户注册逻辑
    # 检查用户名和邮箱是否唯一，如果唯一则进行注册
    # 否则返回注册失败的消息
    # 这里仅作为示例，不包含实际的注册逻辑
    if username == 'example_user' and email == 'example@email.com':
        return jsonify({'message': 'Registration successful'})
    else:
        return jsonify({'message': 'Registration failed'})

# 聊天接口
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    content_id = data.get('contentId')
    user_id = data.get('userId')  # Assuming you have a userId in the request data
    content = data.get('content')

    # 查询数据库获取原始聊天数据
    cursor = conn.cursor()
    cursor.execute("SELECT Content FROM ContentTable WHERE ContentID = ? AND UserID = ?", content_id, user_id)
    current_content = cursor.fetchone()

    if current_content:
        current_content = json.loads(current_content[0])
    else:
        current_content = {}

    # 在当前聊天数据中添加新的内容
    current_content.setdefault(content_id, []).append({
        "role": "user",
        "content": content
    })

    # 更新数据库中的聊天数据
    cursor.execute("UPDATE ContentTable SET Content = ? WHERE ContentID = ? AND UserID = ?", json.dumps(current_content), content_id, user_id)
    conn.commit()

    return jsonify({'message': 'Chat updated successfully'})

if __name__ == '__main__':
    app.run(debug=True)