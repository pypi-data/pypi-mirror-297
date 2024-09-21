# -*- coding: UTF-8 -*-
# python3

import os

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/lang', methods=['GET'])
def handle_lang_get():
    name = request.args.get('name', 'default_name')
    age = request.args.get('age', '0')

    return jsonify({
        'message': 'GET 请求成功',
        'name': name,
        'age': age
    })

@app.route('/lang', methods=['POST'])
def handle_lang_post():
    if request.is_json:
        data = request.get_json()
        name = data.get('name', 'default_name')
        age = data.get('age', 0)

        return jsonify({
            'message': 'POST 请求成功',
            'name': name,
            'age': age
        })
    else:
        return jsonify({'error': '请求数据不是 JSON 格式'}), 400

def cmd_handle(args):
    app.run(host='0.0.0.0', port=8999, debug=True)


def cmd_regist(subparsers):
    parser = subparsers.add_parser('lang.server', help='server to receive feishu push')
    parser.set_defaults(handle=cmd_handle)

# curl "http://127.0.0.1:5000/get_data?name=John&age=30"
# curl -X POST "http://127.0.0.1:5000/post_data" -H "Content-Type: application/json" -d '{"name": "John", "age": 30}'
if __name__ == '__main__':
    cmd_handle({})