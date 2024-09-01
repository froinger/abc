# app.py
from flask import Flask, render_template
import subprocess

app = Flask(__name__)

def msg(status, data='未加载到数据'):
    """
    :param status: 状态码 200成功，201未找到数据
    :param data: 响应数据
    :return: 字典 如{'status': 201, 'data': ‘未加载到数据’}
    """
    return json.dumps({'status': status, 'data': data})

# 定义一个路由来处理按钮点击
@app.route('/')
def index():
    return render_template('index.html')

# 定义一个路由来处理Python文件的执行
@app.route('/run_python_script')
def run_python_script():
    try:
        # 使用subprocess运行Python脚本
        result = subprocess.run(['python', 'your_script.py'], capture_output=True, text=True)
        return f"Script output: {result.stdout}"
    except Exception as e:
        return f"An error occurred: {e}"

@app.route('/nav')
def goto_nav():
    try:
        return render_template('nav.html')
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)