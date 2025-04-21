from typing import Dict, Any, Optional

class BatchCreateBlockedTimeResponse:
    def __init__(self, count: int):
        if not isinstance(count, int):
            # 初期化時の型チェック (より厳密にする場合)
            raise TypeError(f"count は整数である必要がありますが、{type(count)} が指定されました。")
        self.count: int = count

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Optional['BatchCreateBlockedTimeResponse']:
        if not isinstance(data, dict):
            print(f"エラー: from_dict に辞書形式でないデータが渡されました: {type(data)}")
            return None # または raise TypeError("Data must be a dictionary.")

        count_value = data.get("count")

        if count_value is None:
            print("エラー: レスポンス辞書に必要な 'count' キーが見つかりません。")
            # raise ValueError("Response dictionary is missing the 'count' key.")
            return None

        if not isinstance(count_value, int):
            print(f"エラー: 'count' の値が整数ではありません。実際の型: {type(count_value)}")
            return None

        # 必要なデータが揃い、型も正しい場合にインスタンスを生成して返す
        return cls(count=count_value)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(count={self.count})"

