from flask import make_response, jsonify


def make_resp(message, status):
    resp = make_response(message, status)
    resp.headers['Content-type'] = "application/json; charset=utf-8"
    return resp
