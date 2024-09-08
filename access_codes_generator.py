from access_codes_hasher import process_access_codes

import random
import json
import string

def generate_access_codes(num_codes=5000, code_length=12):
    # 紛らわしい文字を除外したキャラクターセット
    characters = ''.join(filter(lambda x: x not in ['O', '0', 'I', 'l'], string.ascii_letters + string.digits))

    access_codes = set()  # 重複を避けるためにセットを使用

    while len(access_codes) < num_codes:
        code = ''.join(random.choice(characters) for _ in range(code_length))
        access_codes.add(code)

    return list(access_codes)

# アクセスコードを生成
access_codes = generate_access_codes()

# JSONファイルに書き込む
with open('etc/secrets/valid_access_codes.json', 'w') as f:
    json.dump({'access_codes': access_codes}, f, indent=4)

# 使用例
input_json_path = 'etc/secrets/valid_access_codes.json'   # 元のJSONファイルのパス
output_json_path = 'etc/secrets/hashed_valid_access_codes.json'  # ハッシュ化されたJSONファイルの保存先
process_access_codes(input_json_path, output_json_path)

print("アクセスコードをハッシュ化して新しいファイルに保存しました。")

print(f'{len(access_codes)}個のアクセスコードが生成され、valid_access_codes.jsonに保存されました。')
