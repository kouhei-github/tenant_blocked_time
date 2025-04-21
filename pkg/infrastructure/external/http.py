import json
import urllib.request
import urllib.error
import urllib.parse # URL結合のために追加
from typing import Dict, Any, Optional, Type # Typeを追加
from pkg.domain.interface.external.http_external import ResponseObjectType, RequestDataType, IHttpRequest

class JsonHttpRequest(IHttpRequest):
    """
    JSONデータの送受信を行う汎用的なHTTPリクエストクラス (urllib使用)。
    インスタンスは特定のRequest/Response型に束縛されない。
    """
    def __init__(self, base_url: str):
        """Initializes with a base URL."""
        if not base_url.endswith('/'):
            base_url += '/'
        self.base_url = base_url
        # print(f"HttpRequest initialized with base URL: {self.base_url}")

    def _prepare_request(
        self,
        endpoint: str,
        data: Any = None, # json.dumps が扱える任意の型を受け入れる
        method: str = "GET",
        headers: Optional[Dict[str, str]] = None
    ) -> urllib.request.Request:
        """内部ヘルパー: リクエストオブジェクトを準備"""
        full_url = urllib.parse.urljoin(self.base_url, endpoint.lstrip('/'))
        final_headers = {'Accept': 'application/json'}
        data_bytes = None
        json_data_string = "" # デバッグ表示用
        if data is not None:
            try:
                json_data_string = json.dumps(data, ensure_ascii=False) # 日本語等を考慮
                data_bytes = json_data_string.encode('utf-8')
                final_headers['Content-Type'] = 'application/json; charset=utf-8'
            except TypeError as e:
                raise ValueError(f"リクエストデータのJSONシリアライズに失敗: {e}") from e
        if headers:
            final_headers.update(headers)

        return urllib.request.Request(full_url, data=data_bytes, headers=final_headers, method=method.upper())

    def do_request(
        self,
        endpoint: str,
        data: Any = None, # 任意のデータ型
        method: str = "POST",
        headers: Optional[Dict[str, str]] = None,
        timeout: int = 10
    ) -> Dict[str, Any]:
        """
        HTTPリクエストを実行し、レスポンスボディをJSONデコードした辞書を返す
        """
        req = self._prepare_request(endpoint, data, method, headers)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as response:
                # status_code = response.status
                # print(f"Response status: {status_code}") # ステータスコードは常に表示すると良い
                response_body_bytes = response.read()
                charset = response.info().get_content_charset() or 'utf-8'
                response_body_string = response_body_bytes.decode(charset)
                # print(f"Raw Response Body: {response_body_string[:500]}...") # デバッグ用

                if not response_body_string:
                    return {}
                try:
                    response_data = json.loads(response_body_string)
                    return response_data
                except json.JSONDecodeError as e:
                    print(f"レスポンスのJSONデコードに失敗: {e}")
                    print(f"受信データ抜粋: {response_body_string[:500]}")
                    raise e
        except urllib.error.HTTPError as e:
            print(f"HTTPエラー発生: {e.code} {e.reason}")
            try:
                error_body = e.read().decode(e.headers.get_content_charset() or 'utf-8', errors='ignore')
                print(f"エラーレスポンスボディ: {error_body}")
                try: e.json_body = json.loads(error_body)
                except json.JSONDecodeError: e.text_body = error_body
            except Exception as read_err: print(f"エラーレスポンスボディの読み取り/デコード失敗: {read_err}")
            raise e # エラーは呼び出し元で処理できるよう再送出
        except urllib.error.URLError as e: print(f"URLエラー発生: {e.reason}"); raise e
        except Exception as e: print(f"予期せぬエラーが発生: {e}"); raise e

    # --- request_and_parse: メソッドレベルでジェネリクスを使用 ---
    def request_and_parse(
        self,
        endpoint: str,
        response_type: Type[ResponseObjectType], # 変換先のクラス型を引数で受け取る
        data: Optional[RequestDataType] = None, # 送信するデータの型 (呼び出し側で決まる)
        method: str = "POST",
        headers: Optional[Dict[str, str]] = None,
        timeout: int = 10
    ) -> Optional[ResponseObjectType]: # 指定されたクラス型のオブジェクトを返す
        """
        リクエストを実行し、レスポンスを指定されたクラスのオブジェクトに変換
        変換には response_type クラスの from_dict クラスメソッドが必要
        """
        # from_dict の存在チェック
        if not hasattr(response_type, 'from_dict') or not callable(getattr(response_type, 'from_dict')):
             raise AttributeError(f"{response_type.__name__} クラスには 'from_dict' クラスメソッドが必要です。")

        try:
            # do_request は辞書を返す
            response_dict = self.do_request(endpoint, data, method, headers, timeout)
            if response_dict:
                # response_type (例: Authentication) の from_dict を呼び出す
                # 型チェッカーも ResponseObjectType を返すと認識できる
                return response_type.from_dict(response_dict)
            else:
                # レスポンスが空だった場合
                print(f"警告: {endpoint} から空のレスポンスを受信しました。")
                return None
        except Exception as e:
            # do_request でエラーが発生した場合、ログはすでに出力されている
            # ここではオブジェクト変換中のエラーとしてログを追加するか、Noneを返す
            print(f"{response_type.__name__} オブジェクトへの変換中またはリクエスト中にエラーが発生しました: {e}")
            # 必要に応じて例外を再送出: raise e
            return None # エラー時は None を返す仕様とする (呼び出し側で要確認)
