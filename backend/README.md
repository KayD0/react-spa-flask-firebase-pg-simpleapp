# クリーンアーキテクチャ バックエンドAPI

Firebase認証を使用したユーザー認証とプロフィール管理機能を提供するFlask APIです。クリーンコードの原則に基づいて設計されています。

## 目次

- [アーキテクチャ概要](#アーキテクチャ概要)
- [技術スタック](#技術スタック)
- [プロジェクト構造](#プロジェクト構造)
- [セットアップ手順](#セットアップ手順)
  - [前提条件](#前提条件)
  - [インストール](#インストール)
  - [APIキーの取得](#apiキーの取得)
- [APIの実行](#apiの実行)
- [APIエンドポイント](#apiエンドポイント)
- [エラーハンドリング](#エラーハンドリング)
- [テスト](#テスト)
- [フロントエンド連携](#フロントエンド連携)
- [開発ガイド](#開発ガイド)
- [トラブルシューティング](#トラブルシューティング)

## アーキテクチャ概要

このバックエンドAPIは以下の設計原則に基づいています：

- **クリーンアーキテクチャ**: 関心事の分離と依存性の方向の制御
- **SOLID原則**: 単一責任、オープン・クローズド、リスコフの置換、インターフェース分離、依存性逆転の原則
- **依存性注入**: コンポーネント間の疎結合を実現
- **型ヒント**: Pythonの型ヒントを使用した静的型チェック
- **包括的なエラーハンドリング**: 一貫性のあるエラーレスポンス
- **構造化ロギング**: JSON形式のログ出力

## 技術スタック

- **Python 3.7+**: サーバーサイド言語
- **Flask**: Webフレームワーク
- **Flask-SQLAlchemy**: ORMとデータベース操作
- **Marshmallow**: データバリデーション
- **Firebase Admin SDK**: IDトークン検証
- **Pytest**: テストフレームワーク

## プロジェクト構造

```
backend/
├── app.py                  # アプリケーションのエントリーポイント
├── config.py               # 設定モジュール
├── errors.py               # エラーハンドリングモジュール
├── logger.py               # ロギングモジュール
├── schemas.py              # バリデーションスキーマ
├── requirements.txt        # 依存関係
├── run_tests.py            # テスト実行スクリプト
├── setup_dev.py            # 開発環境セットアップスクリプト
├── controllers/            # コントローラー（ルートハンドラー）
│   ├── __init__.py
│   ├── auth_controller.py  # 認証関連のエンドポイント
│   ├── main_controller.py  # 基本エンドポイント
│   └── profile_controller.py # プロフィール関連のエンドポイント
├── models/                 # データモデル
│   └── user_profile.py     # ユーザープロフィールモデル
├── services/               # ビジネスロジック
│   ├── __init__.py
│   ├── auth_service.py     # 認証サービス
│   └── db_service.py       # データベースサービス
└── tests/                  # テスト
    └── test_api.py         # APIエンドポイントのテスト
```

## セットアップ手順

### 前提条件

- Python 3.7以上
- PostgreSQL（または別のSQLAlchemyがサポートするデータベース）
- Firebase Admin SDK（認証用）

### インストール

開発環境セットアップスクリプトを使用して簡単にセットアップできます：

```bash
# セットアップスクリプトを実行
python setup_dev.py

# 仮想環境をアクティベート
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

または、手動でセットアップすることもできます：

1. 仮想環境を作成して有効化します：

```bash
# 仮想環境の作成
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

2. 必要な依存関係をインストールします：

```bash
pip install -r requirements.txt
```

3. `.env.example`ファイルを基に`.env`ファイルを作成します：

```bash
cp .env.example .env
```

4. `.env`ファイルを編集し、APIキーと設定を追加します。

### APIキーの取得

#### Firebase認証のセットアップ

1. [Firebase Console](https://console.firebase.google.com/)にアクセスします
2. 新しいプロジェクトを作成するか、既存のプロジェクトを選択します
3. Authentication機能を有効化し、メール/パスワード認証を設定します
4. プロジェクト設定 > サービスアカウントに移動します
5. 「新しい秘密鍵を生成」をクリックしてJSONファイルをダウンロードします
6. JSONファイルの内容を`.env`ファイルの対応する変数に設定します

## APIの実行

Flask開発サーバーを起動します：

```bash
# 直接実行
python app.py
```

APIは`http://localhost:5000`で利用可能になります。

## APIエンドポイント

### 基本エンドポイント

#### GET /

APIが実行中であることを確認するための簡単なメッセージを返します。

**レスポンス例**:
```json
{
  "status": "running",
  "version": "1.0.0",
  "message": "ユーザープロフィールAPIが実行中です",
  "endpoints": {
    "auth_verify": "/api/auth/verify (Authorizationヘッダーを持つPOST)",
    "profile_get": "/api/profile (Authorizationヘッダーを持つGET)",
    "profile_update": "/api/profile (JSONボディとAuthorizationヘッダーを持つPUT)"
  }
}
```

### 認証エンドポイント

#### POST /api/auth/verify

認証トークンを検証し、ユーザー情報を返します。

**リクエストヘッダー**:
```
Authorization: Bearer <firebase_id_token>
```

**レスポンス例**:
```json
{
  "authenticated": true,
  "user": {
    "uid": "user_id",
    "email": "user@example.com",
    "email_verified": true,
    "auth_time": 1648123456
  }
}
```

#### POST /api/auth/token

トークンを検証し、有効かどうかを返します。

**リクエストボディ（JSON）**:
```json
{
  "token": "<firebase_id_token>"
}
```

**レスポンス例**:
```json
{
  "valid": true,
  "user": {
    "uid": "user_id",
    "email": "user@example.com",
    "email_verified": true,
    "auth_time": 1648123456
  }
}
```

### プロフィールエンドポイント

#### GET /api/profile

ユーザーのプロフィール情報を取得します。

**リクエストヘッダー**:
```
Authorization: Bearer <firebase_id_token>
```

**レスポンス例**:
```json
{
  "success": true,
  "profile": {
    "id": 1,
    "firebase_uid": "user_id",
    "display_name": "ユーザー名",
    "bio": "自己紹介",
    "location": "東京",
    "website": "https://example.com",
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-02T00:00:00Z"
  }
}
```

#### PUT /api/profile

ユーザーのプロフィール情報を更新します。

**リクエストヘッダー**:
```
Authorization: Bearer <firebase_id_token>
Content-Type: application/json
```

**リクエストボディ（JSON）**:
```json
{
  "display_name": "新しいユーザー名",
  "bio": "新しい自己紹介",
  "location": "大阪",
  "website": "https://new-example.com"
}
```

**レスポンス例**:
```json
{
  "success": true,
  "profile": {
    "id": 1,
    "firebase_uid": "user_id",
    "display_name": "新しいユーザー名",
    "bio": "新しい自己紹介",
    "location": "大阪",
    "website": "https://new-example.com",
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-03T00:00:00Z"
  },
  "message": "プロフィールが更新されました"
}
```

#### DELETE /api/profile

ユーザーのプロフィールを削除します。

**リクエストヘッダー**:
```
Authorization: Bearer <firebase_id_token>
```

**レスポンス例**:
```json
{
  "success": true,
  "message": "プロフィールが削除されました"
}
```

## エラーハンドリング

APIは一貫性のあるエラーレスポンスを返します：

- **400 Bad Request**: 不正なリクエスト
  ```json
  {
    "error": "bad_request",
    "message": "リクエストが不正です",
    "status_code": 400
  }
  ```

- **401 Unauthorized**: 認証エラー
  ```json
  {
    "error": "unauthorized",
    "message": "認証が必要です",
    "status_code": 401
  }
  ```

- **403 Forbidden**: 権限エラー
  ```json
  {
    "error": "forbidden",
    "message": "このリソースにアクセスする権限がありません",
    "status_code": 403
  }
  ```

- **404 Not Found**: リソースが見つからない
  ```json
  {
    "error": "not_found",
    "message": "指定されたリソースが見つかりません",
    "status_code": 404
  }
  ```

- **422 Unprocessable Entity**: バリデーションエラー
  ```json
  {
    "error": "validation_error",
    "message": "入力データが無効です",
    "status_code": 422,
    "details": {
      "errors": {
        "display_name": ["フィールドは必須です"]
      }
    }
  }
  ```

- **429 Too Many Requests**: レート制限超過
  ```json
  {
    "error": "rate_limit_exceeded",
    "message": "リクエスト制限を超えました。しばらく待ってから再試行してください",
    "status_code": 429
  }
  ```

- **500 Internal Server Error**: サーバーエラー
  ```json
  {
    "error": "internal_error",
    "message": "内部サーバーエラーが発生しました",
    "status_code": 500
  }
  ```

## テスト

このプロジェクトには自動テストが含まれています：

```bash
# すべてのテストを実行
python run_tests.py

# または、pytestを直接使用
pytest tests/
```

テストファイルの概要：

- **tests/test_api.py**: APIエンドポイントのテスト

## フロントエンド連携

このAPIは付属のフロントエンドアプリケーションと連携するように設計されています。フロントエンドには以下が含まれます：

1. Firebase認証を使用したユーザー認証システム
2. ユーザープロフィール管理機能

フロントエンドを実行するには：

1. frontディレクトリに移動します
2. 依存関係をインストールします：`npm install`
3. 開発サーバーを起動します：`npm run dev`
4. `http://localhost:3000`でアプリケーションにアクセスします

## 開発ガイド

### 新しいエンドポイントの追加

1. 適切なコントローラーファイルを選択または新規作成します（`controllers/`ディレクトリ内）
2. Blueprintにルートを追加します：

```python
@blueprint.route('/new-endpoint', methods=['POST'])
@auth_required
def new_endpoint():
    """エンドポイントの説明"""
    # リクエストデータの取得と検証
    data = request.get_json()
    validated_data = SomeSchema.validate_request(data)
    
    # ビジネスロジックの実行
    result = some_service_function(validated_data)
    
    # レスポンスの返却
    return jsonify({
        'success': True,
        'data': result
    }), 200
```

3. 必要に応じて新しいサービスを作成します（`services/`ディレクトリ内）
4. テストを追加します（`tests/`ディレクトリ内）

### 新しいモデルの追加

1. `models/`ディレクトリに新しいPythonファイルを作成します
2. モデルクラスを実装します：

```python
from typing import Dict, Any, Optional
from datetime import datetime
from services.db_service import db

class NewModel(db.Model):
    """新しいモデルの説明"""
    __tablename__ = 'new_models'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, name: str) -> None:
        """初期化"""
        self.name = name
    
    def to_dict(self) -> Dict[str, Any]:
        """辞書形式に変換"""
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
```

3. 対応するスキーマを`schemas.py`に追加します
4. 必要に応じてサービス関数を作成します

## トラブルシューティング

### 一般的な問題と解決策

#### Firebase認証エラー

- **トークン検証エラー**:
  - Firebase Admin SDKの設定が正しいか確認
  - クライアントとサーバーが同じFirebaseプロジェクトを使用しているか確認

- **権限エラー**:
  - ユーザーに必要な権限があるか確認
  - Firebaseルールが適切に設定されているか確認

#### データベース関連のエラー

- **接続エラー**:
  - データベース接続情報が正しいか確認
  - データベースサーバーが実行中か確認

- **マイグレーションエラー**:
  - データベーススキーマが最新か確認

#### CORS関連のエラー

- **CORSエラー**:
  - `CORS_ORIGIN`環境変数が正しく設定されているか確認
  - フロントエンドのURLとバックエンドのCORS設定が一致しているか確認

### ログの確認

問題のトラブルシューティングには、ログを確認することが役立ちます：

```bash
# 環境変数でログレベルを設定
export LOG_LEVEL=DEBUG

# アプリケーションを実行
python app.py
```

また、特定のエンドポイントをcurlコマンドで直接テストすることも有効です：

```bash
# 基本的なエンドポイントのテスト
curl http://localhost:5000/

# 認証が必要なエンドポイントのテスト
curl -X POST \
  -H "Authorization: Bearer YOUR_ID_TOKEN" \
  -H "Content-Type: application/json" \
  http://localhost:5000/api/profile
