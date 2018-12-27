from flask import Flask, render_template, request, jsonify

from spider_.s4 import query

app = Flask(__name__)


@app.route('/translate/', methods=['GET', 'POST'])
def translate():
    if request.method == 'POST':
        print(request.form)  # from, to, keyword
        json_result = query(request.form.get('keyword'),
              request.form.get('from'),
              request.form.get('to'))

        return jsonify(json_result)

    return render_template('translate.html', **locals())


@app.route('/update/<id>/', methods=['PUT', 'PATCH'])
def update(id):
    print(request.remote_addr, '--开始更新 ---', id)
    json_data = request.get_json()  # 获取上传的json数据
    print(json_data)
    return jsonify({'status': 'ok'})


@app.route('/upload_log/', methods=['POST'])
def upload_log():
    print(request.remote_addr, '上传的日志')
    # 上传的日志信息，包含所有的日志变量
    # print('form:', request.form)
    name = request.form.get('name')
    msg = request.form.get('msg')
    level_name = request.form.get('levelname')
    user_id = request.form.get('user_id')

    print(user_id, name, msg, level_name)

    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    app.run(host='10.12.155.80')