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


if __name__ == '__main__':
    app.run()