#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
module docstring:

サーバーの起動とそのインターファイス

"""
# Standard Library
import os
from typing import Any, List, Tuple

from flask import Flask, request, send_file, render_template
from werkzeug.utils import secure_filename
from lgtm import save_with_message, OUTPUT_NAME

"""
設定
"""
# サーバーの URL の取得
_FLASK_URL = os.environ.get("FLASK_URL", "http://localhost:2626")

FILE_COUNT = 0
# アップロードされる拡張子の制限
ALLOWED_EXTENSIONS = set(["jpeg","png", "jpg"])
XLSX_MIMETYPE = ["image/jpeg", "image/png", "image/jpg"]

# アプリ
app = Flask(__name__)


@app.route("/", methods=["GET"])
def get_home() -> Any:
    return render_template("index.html", _url=_FLASK_URL)


@app.route(
    "/lgtm",
    methods=[
        "POST",
    ],
)
def lgtm() -> Any:
    """
    文字を画像に記載するインターフェイス
    
    エンドポイント: {url}/lgtm
    """

    global FILE_COUNT
    msg = request.form.get('msg')
    filebuf = request.files.get("lgtm")
    print(filebuf.mimetype)
    if filebuf is None:
        return "ファイルがないよ", 400
    elif not filebuf.mimetype in XLSX_MIMETYPE:
        return "画像じゃないよ", 415
    print()

    # ファイルのチェック
    if filebuf and allwed_file(str(filebuf.filename)):
        # 危険な文字を削除（サニタイズ処理）
        filename = secure_filename(str(filebuf.filename))
        # ファイルの保存
        check_dirs(["./tmp/"])
        path_tmp = f"./tmp/{FILE_COUNT}_{filename}"
        FILE_COUNT += 1
        filebuf.save(path_tmp)
        
        if msg is None or msg == "":
            mgs = "lgtm"

        # 画像処理
        save_with_message(path_tmp, msg)
        os.remove(path_tmp)

        return send_file(OUTPUT_NAME, attachment_filename=f"{msg}.png", as_attachment=True, mimetype=XLSX_MIMETYPE[1]), 200

    else:
        return "拡張子が違います", 415


@app.route("/test", methods=["GET", "POST"])
def test() -> Tuple[str, int]:
    return "試験成功です。", 200


def allwed_file(filename: str) -> int:
    # .があるかどうかのチェックと、拡張子の確認
    # OKなら１、だめなら0
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def check_dirs(dirs: List[str]) -> None:
    # ディレクトリを作成
    for dir in dirs:
        if not os.path.exists(dir):
            os.makedirs(dir)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 2626)))
