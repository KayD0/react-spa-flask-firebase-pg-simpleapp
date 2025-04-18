# YouTube検索・要約 バックエンドAPI

キーワードを使用してYouTubeビデオを検索し、GoogleのVertex AI Geminiモデルを使用してAI駆動の要約を生成するFlask APIです。Firebase認証を使用してユーザー認証を行い、プロフィール管理機能も提供します。

## 目次

- [機能概要](#機能概要)
- [技術スタック](#技術スタック)
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

## 機能概要

このバックエンドAPIは以下の主要機能を提供します：

- **YouTube検索**: YouTube Data API v3を使用してビデオを検索
- **ビデオ要約**: Vertex AI Geminiモデルを使用してビデオ内容の要約を生成
- **ユーザー認証**: Firebase Admin SDKを使用したIDトークン検証
- **プロフィール管理**: ユーザープロフィール情報の保存と取得
- **CORS対応**: フロントエンドとの安全な通信

## 技術スタック

- **Python 3.7+**: サーバーサイド言語
- **Flask**: Webフレームワーク
- **Blueprint**: モジュール化されたルーティング
- **Firebase Admin SDK**: IDトークン検証
- **YouTube Data API v3**: ビデオ検索と情報取得
- **Vertex AI Gemini**: AI要約生成

## セットアップ手順

### 前提条件

- Python 3.7以上
- YouTube Data API v3が有効なGoogle APIキー
- Vertex AI APIが有効なGoogle Cloudプロジェクト（ビデオ要約用）
- Firebase Admin SDK（認証用）

### インストール

1. リポジトリをクローンします
2. backendディレクトリに移動します
3. 仮想環境を作成して有効化します（推奨）：

```bash
# 仮想環境の作成
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

4. 必要な依存関係をインストールします：

```bash
pip install -r requirements.txt
```

5. `.env.example`ファイルを基に`.env`ファイルを作成します：

```bash
cp .env.example .env
```

6. `.env`ファイルを編集し、APIキーと設定を追加します：

```
# YouTube API認証情報
YOUTUBE_API_KEY=あなたのyoutube_api_keyをここに

# CORS設定
CORS_ORIGIN=http://localhost:3000

# Google Cloud設定
GOOGLE_CLOUD_PROJECT=あなたのgoogle_cloudプロジェクトID
GOOGLE_CLOUD_LOCATION=us-central1
GEMINI_MODEL_ID=gemini-1.5-pro

# Google Cloud認証情報ファイルを指すように環境変数を設定
GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/credentials.json

# Firebase設定
FIREBASE_PROJECT_ID=あなたのfirebaseプロジェクトID
FIREBASE_PRIVATE_KEY_ID=あなたのprivate_key_id
FIREBASE_PRIVATE_KEY=あなたのprivate_key
FIREBASE_CLIENT_EMAIL=あなたのclient_email
FIREBASE_CLIENT_ID=あなたのclient_id
FIREBASE_AUTH_URI=https://accounts.google.com/o/oauth2/auth
FIREBASE_TOKEN_URI=https://oauth2.googleapis.com/token
FIREBASE_AUTH_PROVIDER_X509_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
FIREBASE_CLIENT_X509_CERT_URL=あなたのclient_x509_cert_url
```

### APIキーの取得

#### YouTube APIキー

1. [Google Cloud Console](https://console.cloud.google.com/)にアクセスします
2. 新しいプロジェクトを作成するか、既存のプロジェクトを選択します
3. YouTube Data API v3を有効にします
4. 認証情報（APIキー）を作成します
5. APIキーを`.env`ファイルにコピーします

#### Google CloudとVertex AIのセットアップ

1. [Google Cloud Console](https://console.cloud.google.com/)にアクセスします
2. 新しいプロジェクトを作成するか、既存のプロジェクトを選択します
3. Vertex AI APIを有効にします
4. 適切な権限を持つサービスアカウントを作成します
   - 必要な権限: `Vertex AI User`, `Storage Object Viewer`
5. サービスアカウントキーJSONファイルをダウンロードします
6. `GOOGLE_APPLICATION_CREDENTIALS`環境変数をこのファイルを指すように設定します
7. Google CloudプロジェクトIDで`.env`ファイルを更新します

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

# または、Windowsの場合
setup.bat

# または、macOS/Linuxの場合
./setup.sh
```

APIは`http://localhost:5000`で利用可能になります。

## APIエンドポイント

### 基本エンドポイント

#### GET /

APIが実行中であることを確認するための簡単なメッセージを返します。

**レスポンス例**:
```json
{
  "message": "YouTube Search and Summary API is running"
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
  "user": {
    "uid": "user_id",
    "email": "user@example.com",
    "email_verified": true,
    "auth_time": 1648123456
  }
}
```

### 検索エンドポイント

#### POST /api/search

キーワードに基づいてYouTubeビデオを検索します。

**リクエストヘッダー**:
```
Authorization: Bearer <firebase_id_token>
Content-Type: application/json
```

**リクエストボディ（JSON）**:
```json
{
  "q": "python チュートリアル",
  "max_results": 5,
  "channel_id": "UC_x5XG1OV2P6uZZ5FSM9Ttw",
  "published_after": "2023-01-01T00:00:00Z"
}
```

**パラメータ**:
- `q`: 検索クエリ（必須）
- `max_results`: 返す結果の最大数（オプション、デフォルト：10）
- `channel_id`: チャンネルIDでフィルタリング（オプション）
- `published_after`: この日付以降に公開されたビデオでフィルタリング（オプション、ISO 8601形式）

**レスポンス例**:
```json
{
  "query": "python チュートリアル",
  "count": 5,
  "videos": [
    {
      "id": "video_id",
      "title": "Python初心者向けチュートリアル",
      "description": "この包括的なチュートリアルでPythonプログラミングを学びましょう...",
      "thumbnail": "https://i.ytimg.com/vi/video_id/mqdefault.jpg",
      "channel_title": "プログラミングチャンネル",
      "published_at": "2023-01-01T00:00:00Z",
      "view_count": "1.2M",
      "like_count": "45K",
      "comment_count": "1.5K",
      "url": "https://www.youtube.com/watch?v=video_id"
    },
    // その他のビデオ...
  ]
}
```

### 要約エンドポイント

#### POST /api/summarize

Vertex AI Geminiを使用してYouTubeビデオの要約を生成します。

**リクエストヘッダー**:
```
Authorization: Bearer <firebase_id_token>
Content-Type: application/json
```

**リクエストボディ（JSON）**:
```json
{
  "video_id": "dQw4w9WgXcQ"
}
```

**パラメータ**:
- `video_id`: YouTubeビデオID（必須）

**レスポンス例**:
```json
{
  "brief_summary": "このビデオは初心者向けのPythonプログラミングの包括的なチュートリアルで、基本的な構文、データ型、制御構造をカバーしています。",
  "key_points": [
    "Pythonは高水準のインタープリタ型プログラミング言語です",
    "変数は明示的な型宣言が不要です",
    "Pythonは中括弧の代わりにインデントを使用してコードブロックを表します",
    "この言語にはライブラリとフレームワークの豊富なエコシステムがあります"
  ],
  "main_topics": [
    "Python基礎",
    "データ型",
    "制御フロー",
    "関数"
  ],
  "video_id": "dQw4w9WgXcQ",
  "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
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
  "profile": {
    "uid": "user_id",
    "display_name": "ユーザー名",
    "email": "user@example.com",
    "created_at": "2023-01-01T00:00:00Z",
    "last_login": "2023-01-02T00:00:00Z"
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
  "preferences": {
    "theme": "dark",
    "language": "ja"
  }
}
```

**レスポンス例**:
```json
{
  "message": "プロフィールが更新されました",
  "profile": {
    "uid": "user_id",
    "display_name": "新しいユーザー名",
    "email": "user@example.com",
    "preferences": {
      "theme": "dark",
      "language": "ja"
    },
    "updated_at": "2023-01-03T00:00:00Z"
  }
}
```

## エラーハンドリング

APIは適切なエラーメッセージとステータスコードを返します：

- **400 Bad Request**: 必須パラメータの欠落や無効なパラメータ
  ```json
  {
    "error": "必須パラメータ 'q' が欠落しています",
    "status_code": 400
  }
  ```

- **401 Unauthorized**: 認証エラー（トークンなし、無効なトークン）
  ```json
  {
    "error": "認証が必要です",
    "status_code": 401
  }
  ```

- **403 Forbidden**: 権限エラー
  ```json
  {
    "error": "このリソースにアクセスする権限がありません",
    "status_code": 403
  }
  ```

- **404 Not Found**: リソースが見つからない
  ```json
  {
    "error": "指定されたリソースが見つかりません",
    "status_code": 404
  }
  ```

- **429 Too Many Requests**: レート制限超過
  ```json
  {
    "error": "リクエスト制限を超えました。しばらく待ってから再試行してください",
    "status_code": 429
  }
  ```

- **500 Internal Server Error**: サーバーエラー
  ```json
  {
    "error": "内部サーバーエラーが発生しました",
    "status_code": 500
  }
  ```

## テスト

このプロジェクトには自動テストが含まれています：

```bash
# すべてのテストを実行
pytest

# 特定のテストファイルを実行
pytest test_api.py
pytest test_auth.py
```

テストファイルの概要：

- **test_api.py**: API機能のテスト（検索、要約など）
- **test_auth.py**: 認証機能のテスト（トークン検証など）

## フロントエンド連携

このAPIは付属のフロントエンドアプリケーションと連携するように設計されています。フロントエンドには以下が含まれます：

1. カードレイアウトで結果を表示するYouTubeビデオ検索コンポーネント
2. Vertex AI Geminiを使用して要約を生成するビデオ要約コンポーネント
3. Firebase認証を使用したユーザー認証システム
4. ユーザープロフィール管理機能

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
@require_auth
def new_endpoint():
    # リクエストデータの取得
    data = request.get_json()
    
    # ビジネスロジックの実行
    result = some_service.do_something(data)
    
    # レスポンスの返却
    return jsonify(result), 200
```

3. 必要に応じて新しいサービスを作成します（`services/`ディレクトリ内）
4. テストを追加します

### 新しいサービスの追加

1. `services/`ディレクトリに新しいPythonファイルを作成します
2. サービスクラスまたは関数を実装します：

```python
class NewService:
    def __init__(self, config):
        self.config = config
        # 初期化コード
    
    def do_something(self, data):
        # ビジネスロジックの実装
        return result
```

3. コントローラーからサービスをインポートして使用します

## トラブルシューティング

### 一般的な問題と解決策

#### YouTube API関連のエラー

- **APIキーが無効**:
  - Google Cloud Consoleで正しいAPIキーを確認
  - APIキーの制限が適切に設定されているか確認
  - YouTube Data API v3が有効になっているか確認

- **クォータ超過**:
  - Google Cloud Consoleでクォータ使用状況を確認
  - 必要に応じてクォータの増加をリクエスト
  - リクエスト数を減らすようにアプリケーションを調整

#### Vertex AI関連のエラー

- **認証エラー**:
  - `GOOGLE_APPLICATION_CREDENTIALS`環境変数が正しく設定されているか確認
  - サービスアカウントに適切な権限があるか確認

- **モデルエラー**:
  - Vertex AI APIが有効になっているか確認
  - モデルIDが正しいか確認（`GEMINI_MODEL_ID`環境変数）
  - リクエストの形式が正しいか確認

#### Firebase認証エラー

- **トークン検証エラー**:
  - Firebase Admin SDKの設定が正しいか確認
  - クライアントとサーバーが同じFirebaseプロジェクトを使用しているか確認

- **権限エラー**:
  - ユーザーに必要な権限があるか確認
  - Firebaseルールが適切に設定されているか確認

#### CORS関連のエラー

- **CORSエラー**:
  - `CORS_ORIGIN`環境変数が正しく設定されているか確認
  - フロントエンドのURLとバックエンドのCORS設定が一致しているか確認

### ログの確認

問題のトラブルシューティングには、ログを確認することが役立ちます：

```bash
# アプリケーションを詳細なログモードで実行
python app.py --debug
```

また、特定のエンドポイントをcurlコマンドで直接テストすることも有効です：

```bash
# 基本的なエンドポイントのテスト
curl http://localhost:5000/

# 認証が必要なエンドポイントのテスト
curl -X POST \
  -H "Authorization: Bearer YOUR_ID_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"q":"python tutorial"}' \
  http://localhost:5000/api/search
