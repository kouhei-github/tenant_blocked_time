from typing import Dict, Any, Optional

class User:
    def __init__(self, tenantId: Optional[str], email: Optional[str], name: Optional[str], id: Optional[str]):
        self.tenantId, self.email, self.name, self.id = tenantId, email, name, id

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        if not isinstance(data, dict):
            # TypeErrorのメッセージを日本語化
            raise TypeError("ユーザーデータは辞書形式である必要があります")
        return cls(data.get('tenantId'), data.get('email'), data.get('name'), data.get('id'))

    def __repr__(self):
        # __repr__ は通常デバッグ用なので英語のままが一般的ですが、必要なら日本語化も可能です
        # 例: return f"User(ID='{self.id}', 名前='{self.name}', メール='{self.email}')"
        return f"User(id='{self.id}', name='{self.name}', email='{self.email}')"


class Authentication:
    def __init__(self, organizationId: Optional[str], user: Optional[User], refreshToken: Optional[str], accessToken: Optional[str]):
        self.organizationId, self.user, self.refreshToken, self.accessToken = organizationId, user, refreshToken, accessToken

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Authentication':
        if not isinstance(data, dict):
             # TypeErrorのメッセージを日本語化
            raise TypeError("認証データは辞書形式である必要があります")

        user_obj = None
        user_data = data.get('user')
        if isinstance(user_data, dict):
            try:
                user_obj = User.from_dict(user_data)
            except TypeError as e:
                # print 文のメッセージを日本語化
                print(f"警告: Userオブジェクトの生成に失敗しました: {e}")
                # ユーザーオブジェクトの生成失敗が致命的でない場合は処理を続ける
                # 致命的な場合はここで例外を再送出するなど検討
        # Check for essential fields before returning
        access_token = data.get('accessToken')
        # 必要なら必須チェック (コメントアウトされたValueErrorメッセージも日本語化)
        # if not access_token:
        #    raise ValueError("レスポンスに accessToken が見つかりません")
        return cls(data.get('organizationId'), user_obj, data.get('refreshToken'), access_token)

    def __repr__(self):
        user_name = self.user.name if self.user else 'N/A'
        # こちらもデバッグ用途を考慮し英語のままが自然かもしれませんが、変更は可能です
        # 例: return f"Authentication(ユーザー='{user_name}', 組織ID='{self.organizationId}')"
        return f"Authentication(user='{user_name}', orgId='{self.organizationId}')"
