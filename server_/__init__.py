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


if __name__ == '__main__':
    app.run(host='10.12.155.80')