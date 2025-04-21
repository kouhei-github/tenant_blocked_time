from typing import Optional, List, Dict

from pkg.domain.interface.external.http_external import IHttpRequest
from pkg.domain.model.blocked_time import BatchCreateBlockedTimeResponse
from pkg.domain.model.user import Authentication


class ApiUseCase:
    """
    APIとのやり取りを行うユースケース。
    具体的なHTTPクライアントの実装ではなく、IHttpRequestインターフェースに依存させた
    """
    def __init__(self, http_requester: IHttpRequest): # <- インターフェースを型ヒントに指定
        self._requester = http_requester

    def login(self, email: str, password: str) -> Optional[Authentication]:
        """ログインAPIを呼び出す"""
        login_endpoint = "/public/auth/login"
        payload = {"email": email, "password": password}
        # 注入された requester を使用
        auth_obj = self._requester.request_and_parse(
            endpoint=login_endpoint,
            response_type=Authentication,
            data=payload,
            method="POST"
        )
        if auth_obj and auth_obj.accessToken:
            print("ログイン成功")
        else:
            print("ログイン失敗")
        return auth_obj

    def register_blocked_times(
        self,
        access_token: str,
        blocked_times: List[Dict[str, str]]
        ) -> Optional[BatchCreateBlockedTimeResponse]:
        """ブロック時間登録APIを呼び出す"""
        blocked_times_endpoint = "/blocked-times"
        headers = {"Authorization": f"Bearer {access_token}"}
        # 注入された requester を使用
        response_obj = self._requester.request_and_parse(
            endpoint=blocked_times_endpoint,
            response_type=BatchCreateBlockedTimeResponse,
            data=blocked_times,
            method="POST",
            headers=headers
        )
        if response_obj:
            print(f"ブロック時間登録API 成功: {response_obj}")
        else:
            print("失敗: ブロック時間登録API")
        return response_obj

