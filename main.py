import os
import sys
from dotenv import load_dotenv # dotenvからload_dotenvをインポート
from pkg.application.api_use_case import ApiUseCase
from pkg.domain.interface.external.http_external import IHttpRequest
from pkg.infrastructure.external.http import JsonHttpRequest

# --- 環境変数から API ベース URL を読み込む ---
load_dotenv()
env_var_name = 'API_BASE_URL'
api_base_url = os.getenv("API_BASE_URL") # .envファイルの内容も読み込まれる

if api_base_url is None:
    raise Exception("エラー: 環境変数 '{env_var_name}' が環境または .env ファイルに設定されていません。")

def main():
    # APIのエンドポイント情報
    http_client: IHttpRequest = JsonHttpRequest(api_base_url) # 型ヒントはインターフェース

    # ユースケースに必要な依存関係 (http_client) を注入してサービスを生成
    api_use_case = ApiUseCase(http_requester=http_client)

    # ログイン情報
    # TODO: スプレッドシートのA列に店舗名があります。
    login_payload = [{
        "name": "テスト テナント",
        "password": "sfdcj125",
        "email": "takahashi.kentaro1@gmail.com"
    }]

    for payload in login_payload:
        # ユースケースを利用してビジネスロジックを実行
        authentication = api_use_case.login(payload["email"], payload["password"])
        if authentication and authentication.accessToken:
            # ログイン成功後、取得したトークンを使って他のAPIを呼び出す
            times_to_block = [
                {"reason": "サービスからのテスト", "startTime": "2025-04-23T01:00:00Z", "endTime": "2025-04-23T02:00:00Z"}
            ]
            api_use_case.register_blocked_times(authentication.accessToken, times_to_block)
        else:
            print("ログインに失敗したため、後続処理をスキップします。")


if __name__ == "__main__":
    main()
