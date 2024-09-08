import hashlib
import json

# アクセスコードをソルトとともにハッシュ化する関数（前と同じ）
def hash_code(code: str, salt: bytes) -> str:
    return hashlib.sha256(salt + code.encode()).hexdigest()

# 保管されたアクセスコードと一致するか確認する関数
def verify_code(provided_code: str, stored_code: str) -> bool:
    # ストレージからソルトとハッシュを分離
    salt, stored_hash = stored_code.split(':')
    # ソルトをバイト型に変換
    salt = bytes.fromhex(salt)
    # 提供されたアクセスコードをハッシュ化
    new_hash = hash_code(provided_code, salt)
    # ハッシュが一致するか確認
    return new_hash == stored_hash

# 保管されたハッシュ化されたコードのうちマッチするものを返す
def matched_hashed_code(user_code: str, stored_codes_json_path: str) -> bool:
    # 保管されたハッシュ化済みアクセスコードを読み込み
    with open(stored_codes_json_path, 'r') as infile:
        data = json.load(infile)
    
    # 保管された各アクセスコードと照合
    for stored_code in data["access_codes"]:
        if verify_code(user_code, stored_code):
            return stored_code  # 一致した場合
    return None  # 一致しない場合