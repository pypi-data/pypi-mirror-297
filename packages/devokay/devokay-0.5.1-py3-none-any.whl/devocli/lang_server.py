# -*- coding: UTF-8 -*-
# python3

import hashlib
import json
import os
from datetime import datetime

from flask import Flask, request, jsonify
from devolib.util_log import LOG_D

app = Flask(__name__)

'''''''''''''''''''''''''''''''''''''''''''''
# sample
'''

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
    
''''''''''''''''''''''''''''''''''''''''''''''
# xxxxx
'''

# 获取当前日期并生成文件夹名
def get_folder_name():
    today = datetime.today().strftime('%Y-%m-%d')
    folder_path = os.path.join(os.getcwd(), today)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return folder_path

# 生成MD5哈希值
def generate_md5():
    today = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    md5_hash = hashlib.md5(today.encode()).hexdigest()
    return md5_hash

def save_dict_to_file(result_dict, file_md5, lang):
    folder_name = get_folder_name()

    # 生成文件路径
    file_path = os.path.join(folder_name, f"{file_md5}-{lang}.json")
    json_data = json.dumps(result_dict, indent=4)

    # 将字典写入 JSON 文件
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json_file.write(json_data)

# 处理表单数据并保存为JSON文件
def process_form_data(form):
    file_md5 = generate_md5()

    # end_values = form.get('end', '').split(',')
    key_values = form.get('key', '').split(',')

    for lang_key in form:
        if lang_key == 'end' or lang_key == 'key':
            continue

        lang_values = form.get(lang_key, '').split(',')
        result_dict = dict(zip(key_values, lang_values))
        save_dict_to_file(result_dict, file_md5, lang_key)
    
    return file_md5
    
@app.route('/lang/post-pcsdk', methods=['POST'])
def handle_lang_post_pcsdk():
    LOG_D(f'Headers: {request.headers}')
    LOG_D(f'Args: {request.args}')
    LOG_D(f'Form: {request.form}')
    LOG_D(f'Data: {request.data}')
    # LOG_D(f'JSON: {request.json}')

    # Headers: Host: 121.43.228.92:8999
    #         User-Agent: Go-http-client/1.1
    #         Content-Length: 587
    #         Content-Type: multipart/form-data; boundary=e3f349d9b616b840a783a41d7a787ba730b01e667303be74b093647ac4a9
    #         X-Tt-Env: prod
    #         X-Tt-Logid: 02172683097957600000000000000000000ffffd572275b1f1a1f
    #         Accept-Encoding: gzip
    # Args: ImmutableMultiDict([])
    # Form: ImmutableMultiDict([('end', 'pcsdk,pcsdk,pcsdk,pcsdk,pcsdk,pccsdk'), ('key', 'err.timeout,err.eula_get_failed,err.browser_start,err.failed111,err.failed222,err.failed333')])
    # Data: b''

    # 将 ImmutableMultiDict 转换为普通的字典
    # form_data = request.form.to_dict()

    try:
        md5 = process_form_data(request.form)

        return jsonify({
            'data': { 'md5': md5 },
            'code': 0,
            'msg': 'ok'
        })
    except:
        return jsonify({'error': '错误'}), 400

def cmd_handle(args):
    app.run(host='0.0.0.0', port=8999, debug=True)

def cmd_regist(subparsers):
    parser = subparsers.add_parser('lang.server', help='server to receive feishu push')
    parser.set_defaults(handle=cmd_handle)

# curl "http://127.0.0.1:5000/get_data?name=John&age=30"
# curl -X POST "http://127.0.0.1:5000/post_data" -H "Content-Type: application/json" -d '{"name": "John", "age": 30}'
if __name__ == '__main__':
    cmd_handle({})