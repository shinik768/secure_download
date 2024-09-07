from flask import Flask, render_template, request, send_file, redirect, url_for, flash
import json
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'abc')

# パスコードリストのファイルパス
VALID_ACCESS_CODES_FILE = 'valid_access_codes.json'
USED_ACCESS_CODES_FILE = 'used_access_codes.json'

# PDFファイルのパス
PDF_FILE_PATH = 'static/myfile.pdf'

# JSONファイルからパスコードを読み込む関数
def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

# JSONファイルにパスコードを保存する関数
def save_json(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f)

@app.route('/', methods=['GET', 'POST'])
def download_page():
    if request.method == 'POST':
        access_code = request.form.get('access_code')

        # パスコードリストと使用済みパスコードを読み込む
        valid_access_codes = load_json(VALID_ACCESS_CODES_FILE).get('access_codes', [])
        used_access_codes = load_json(USED_ACCESS_CODES_FILE).get('used_access_codes', [])

        # パスコードが有効かどうかを確認
        if access_code in valid_access_codes and access_code not in used_access_codes:
            # 使用済みパスコードとして登録
            used_access_codes.append(access_code)
            save_json({'used_access_codes': used_access_codes}, USED_ACCESS_CODES_FILE)

            # PDFファイルを送信
            return send_file(PDF_FILE_PATH, as_attachment=True)

        else:
            flash('無効なアクセスコードです。', 'error')
            return redirect(url_for('download_page'))

    return render_template('download.html')

if __name__ == '__main__':
    # アプリを実行
    app.run(debug=True)
