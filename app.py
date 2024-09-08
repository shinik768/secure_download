from AES_decrypter import execute_decrypt
from matched_hashed_access_codes_provider import matched_hashed_code
from flask import Flask, render_template, request, send_file, redirect, url_for, flash, session, render_template_string
import json
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# パスコードリストのファイルパス
HASHED_VALID_ACCESS_CODES_FILE = '/etc/secrets/hashed_valid_access_codes.json'
HASHED_USED_ACCESS_CODES_FILE = 'hashed_used_access_codes.json'

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
    if session.get('access_code_valid'):
        return render_template('download_link.html')
    
    if request.method == 'POST':
        access_code = request.form.get('access_code')

        # パスコードリストと使用済みパスコードを読み込む
        used_access_codes = load_json(HASHED_USED_ACCESS_CODES_FILE).get('access_codes', [])

        # パスコードが有効かどうかを確認
        matched_valid_hash_code = matched_hashed_code(access_code, HASHED_VALID_ACCESS_CODES_FILE)
        matched_used_hash_code = matched_hashed_code(access_code, HASHED_USED_ACCESS_CODES_FILE)
        if matched_valid_hash_code is not None and matched_used_hash_code is None:
            # 使用済みパスコードとして登録
            used_access_codes.append(matched_valid_hash_code)
            save_json({'access_codes': used_access_codes}, HASHED_USED_ACCESS_CODES_FILE)

            # セッションにフラグを設定
            session['access_code_valid'] = True
            
            # ダウンロード用のリンクを提供
            return redirect(url_for('download_link'))

        else:
            flash('無効なアクセスコードです。', 'error')
            return redirect(url_for('download_page'))

    return render_template('download.html')

@app.route('/<access_code>')
def check_access_code(access_code):
    if session.get('access_code_valid'):
        return render_template('download_link.html')
    
    # パスコードリストと使用済みパスコードを読み込む
    used_access_codes = load_json(HASHED_USED_ACCESS_CODES_FILE).get('access_codes', [])

    # パスコードが有効かどうかを確認
    matched_valid_hash_code = matched_hashed_code(access_code, HASHED_VALID_ACCESS_CODES_FILE)
    matched_used_hash_code = matched_hashed_code(access_code, HASHED_USED_ACCESS_CODES_FILE)
    if matched_valid_hash_code is not None and matched_used_hash_code is None:
        # 使用済みパスコードとして登録
        used_access_codes.append(matched_valid_hash_code)
        save_json({'access_codes': used_access_codes}, HASHED_USED_ACCESS_CODES_FILE)

        # セッションにフラグを設定
        session['access_code_valid'] = True
        
        # ダウンロード用のリンクを提供
        return redirect(url_for('download_link'))

    else:
        return render_template_string("<h1>無効なページです。</h1>")

@app.route('/download_link')
def download_link():
    # アクセスコードが有効かを確認
    if session.get('access_code_valid'):
        return render_template('download_link.html')
    else:
        flash('無効なアクセスです。', 'error')
        return redirect(url_for('download_page'))

@app.route('/download_complete_page')
def download_complete_page():
    return render_template('download_complete.html')

@app.route('/download_file')
def download_file():
    # セッションでアクセスコードが有効かを確認
    if session.get('access_code_valid'):
        decrypted_pdf_stream = execute_decrypt()
        # ストリームのカーソルを先頭に戻す
        decrypted_pdf_stream.seek(0)
        # PDFをブラウザの別タブで表示するためのリダイレクト
        return send_file(decrypted_pdf_stream, download_name='HUB.pdf', as_attachment=True, mimetype="application/pdf")
    else:
        flash('無効なアクセスです。', 'error')
        return redirect(url_for('download_page'))

if __name__ == "__main__":
    port = int(os.getenv("PORT"))  # ポート番号を環境変数から取得
    app.run(host='0.0.0.0', port=port)  # Flaskアプリを起動