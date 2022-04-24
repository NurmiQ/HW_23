import os
from flask import Flask, request
from werkzeug.exceptions import BadRequest

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


def build_query(it, cmd, value):
    res = map(lambda v: v.strip(), it)
    if cmd == "filter":
        res = filter(lambda v, txt=value: txt in v, res)
    if cmd == "map":
        arg = int(value)
        res = map(lambda v, idx=arg: v.split(" ")[idx], res)
    if cmd == "unique":
        res = set(res)
    if cmd == "sort":
        reverse = value == "desc"
        res = sorted(res, reverse=reverse)
    if cmd == "limit":
        arg = int(value)
        res = list(res[:arg])
    return res


@app.route("/perform_query")
def perform_query():
    try:
        cmd1 = request.args.get["cmd_1"]
        cmd2 = request.args.get["cmd_2"]
        value1 = request.args.get["value_1"]
        value2 = request.args.get["value_2"]
        file_name = request.args.get("file_name")
    except KeyError:
        raise BadRequest

    file_path = os.path.join(DATA_DIR, file_name)
    if not os.path.exists(file_path):
        return BadRequest(description=f"{file_name} does not exist")

    with open(file_path) as fp:
        res = build_query(fp, cmd1, value1)
        res = build_query(fp, cmd2, value2)
        content = '\n'.join(res)


    # получить параметры query и file_name из request.args, при ошибке вернуть ошибку 400
    # проверить, что файла file_name существует в папке DATA_DIR, при ошибке вернуть ошибку 400
    # с помощью функционального программирования (функций filter, map), итераторов/генераторов сконструировать запрос
    # вернуть пользователю сформированный результат
    return app.response_class(content, content_type="text/plain")
