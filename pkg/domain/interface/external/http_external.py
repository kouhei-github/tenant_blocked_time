# core/http_interface.py (例: ファイルパス)

from abc import ABC, abstractmethod
from typing import TypeVar, Dict, Any, Optional, Type, List # Listを追加

# --- TypeVars (インターフェース定義で必要) ---
RequestDataType = TypeVar('RequestDataType')
ResponseObjectType = TypeVar('ResponseObjectType')

class IHttpRequest(ABC):
    @abstractmethod
    def do_request(
        self,
        endpoint: str,
        data: Any = None,
        method: str = "POST",
        headers: Optional[Dict[str, str]] = None,
        timeout: int = 10
    ) -> Dict[str, Any]:
        """
        HTTPリクエストを実行し、レスポンスボディをJSONデコードした辞書として返す

        Args:
            endpoint (str): リクエスト先の相対エンドポイントパス。
            data (Any): リクエストボディとして送信するデータ (JSONシリアライズ可能なもの)。
            method (str): HTTPメソッド。
            headers (Optional[Dict[str, str]]): 追加/上書きするHTTPヘッダー。
            timeout (int): タイムアウト秒数。

        Returns:
            Dict[str, Any]: JSONレスポンスボディの辞書表現。

        Raises:
            Exception: 通信エラー、HTTPエラー、デコードエラーなどが発生した場合。
                       具体的な例外型は実装クラスに依存します。
        """
        # ABCのメソッドは実装を持たない (pass または NotImplementedError を記述)
        raise NotImplementedError

    @abstractmethod
    def request_and_parse(
        self,
        endpoint: str,
        response_type: Type[ResponseObjectType], # 変換先のクラス型
        data: Optional[RequestDataType] = None, # 送信するデータの型
        method: str = "POST",
        headers: Optional[Dict[str, str]] = None,
        timeout: int = 10
    ) -> Optional[ResponseObjectType]: # 指定されたクラス型のオブジェクト
        """
        HTTPリクエストを実行し、レスポンスを指定された型のオブジェクトにパースして返します。
        パースには `response_type` クラスに `from_dict` クラスメソッドが必要です。

        Args:
            endpoint (str): リクエスト先の相対エンドポイントパス。
            response_type (Type[ResponseObjectType]): レスポンスをパースする先のクラス型。
            data (Optional[RequestDataType]): リクエストボディデータ。
            method (str): HTTPメソッド。
            headers (Optional[Dict[str, str]]): HTTPヘッダー。
            timeout (int): タイムアウト秒数。

        Returns:
            Optional[ResponseObjectType]: パースされたレスポンスオブジェクト。
                                          エラー発生時や空レスポンス時は None を返すことがあります。

        Raises:
            AttributeError: `response_type` に `from_dict` が実装されていない場合。
            Exception: 通信エラー、HTTPエラー、パースエラーなどが発生した場合。
                       具体的な例外型は実装クラスに依存します。
        """
        raise NotImplementedError
