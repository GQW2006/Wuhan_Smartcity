from flask import jsonify

def ok(data=None):
    return jsonify({'code': 0, 'msg': 'success', 'data': data})

def fail(msg='error',http=404):
    return jsonify({'code': 20001, 'msg': msg, 'data': None}),http
