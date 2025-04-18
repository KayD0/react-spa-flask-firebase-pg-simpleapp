# React SPA Flask Postgres Simple App

Firebase認証を使用したピュアJSのシンプルなFlaskウェブアプリケーション

## 目次

- [概要](#概要)
- [主な機能](#主な機能)
- [技術スタック](#技術スタック)
- [システムアーキテクチャ](#システムアーキテクチャ)
- [セットアップ手順](#セットアップ手順)
  - [前提条件](#前提条件)
  - [APIキーの取得](#apiキーの取得)
  - [バックエンドのセットアップ](#バックエンドのセットアップ)
  - [フロントエンドのセットアップ](#フロントエンドのセットアップ)
- [開発ガイド](#開発ガイド)
- [使用方法](#使用方法)
- [プロジェクト構造](#プロジェクト構造)
- [トラブルシューティング](#トラブルシューティング)
- [ライセンス](#ライセンス)

## 概要

このアプリケーションは、ユーザーがFirebase認証でログインし、YouTubeビデオを検索して、選択したビデオの内容をVertex AI Geminiを使用して要約する機能を提供します。バックエンドはFlaskで実装され、フロントエンドはVanilla JSとBootstrapで構築されています。

## 主な機能

- **ユーザー認証**: Firebase Authenticationを使用したユーザー登録・ログイン機能
- **認証トークン検証**: バックエンドでのFirebase IDトークン検証
- **レスポンシブUI**: モバイルデバイスにも対応したユーザーインターフェース
- **プロフィール管理**: ユーザープロフィール情報の管理機能

## 技術スタック

### フロントエンド

- **HTML/CSS/JavaScript**: 基本的なWeb技術
- **Bootstrap 5**: UIコンポーネントとレスポンシブデザイン
- **Vite**: モジュールバンドラー・開発サーバー
- **Firebase SDK**: 認証とIDトークン管理
- **SCSS**: スタイリングの拡張機能

### バックエンド

- **Python 3.7+**: サーバーサイド言語
- **Flask**: Webフレームワーク
- **Blueprint**: モジュール化されたルーティング
- **Firebase Admin SDK**: IDトークン検証

### クラウドサービス

- **Firebase Authentication**: ユーザー認証

## セットアップ手順

### 前提条件

- Python 3.7以上
- Node.js 14以上
- npm または yarn
- Google Cloudアカウント
- Firebaseプロジェクト


#### Firebase設定

1. [Firebase Console](https://console.firebase.google.com/)にアクセス
2. プロジェクトを作成または選択
3. Authentication機能を有効化し、メール/パスワード認証を設定
4. プロジェクト設定からWebアプリを追加
5. 提供されるFirebase設定オブジェクトをコピー
6. プロジェクト設定 > サービスアカウントから新しい秘密鍵を生成


### バックエンドのセットアップ

1. リポジトリをクローン:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. バックエンドディレクトリに移動:
   ```bash
   cd backend
   ```

3. 仮想環境を作成して有効化:
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

4. 依存関係をインストール:
   ```bash
   pip install -r requirements.txt
   ```

5. `.env.example`をコピーして`.env`ファイルを作成:
   ```bash
   cp .env.example .env
   ```

6. `.env`ファイルを編集し、必要な環境変数を設定:
   ```
   # CORS設定
   CORS_ORIGIN=http://localhost:3000

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

7. バックエンドサーバーを起動:
   ```bash
   # Windows
   python app.py
   # または
   setup.bat

   # macOS/Linux
   python app.py
   # または
   ./setup.sh
   ```
   サーバーは`http://localhost:5000`で実行されます。

### フロントエンドのセットアップ

1. フロントエンドディレクトリに移動:
   ```bash
   cd front
   ```

2. 依存関係をインストール:
   ```bash
   npm install
   # または
   yarn
   ```

3. `.env.example`をコピーして`.env`ファイルを作成:
   ```bash
   cp .env.example .env
   ```

4. `.env`ファイルを編集し、Firebase設定を追加:
   ```
   VITE_FIREBASE_API_KEY=あなたのapiKey
   VITE_FIREBASE_AUTH_DOMAIN=あなたのauthDomain
   VITE_FIREBASE_PROJECT_ID=あなたのprojectId
   VITE_FIREBASE_STORAGE_BUCKET=あなたのstorageBucket
   VITE_FIREBASE_MESSAGING_SENDER_ID=あなたのmessagingSenderId
   VITE_FIREBASE_APP_ID=あなたのappId
   
   VITE_API_BASE_URL=http://localhost:5000
   ```

5. 開発サーバーを起動:
   ```bash
   npm run dev
   # または
   yarn dev
   ```
   フロントエンドは`http://localhost:3000`で実行されます。

## 開発ガイド

### バックエンド開発

- **コントローラーの追加**:
  1. `backend/controllers/`に新しいコントローラーファイルを作成
  2. Blueprintを定義し、ルートを設定
  3. 必要なサービスをコントローラー内で初期化
  4. `app.py`でBlueprintを登録

- **サービスの追加**:
  1. `backend/services/`に新しいサービスファイルを作成
  2. 必要なクラスとメソッドを実装
  3. コントローラーからサービスをインポートして使用

- **テスト**:
  1. `test_api.py`と`test_auth.py`を参考にテストを作成
  2. `pytest`を使用してテストを実行

### フロントエンド開発

- **コンポーネントの追加**:
  1. `front/src/js/components/`に新しいコンポーネントファイルを作成
  2. 必要なHTMLとJavaScriptを実装
  3. メインアプリケーションからコンポーネントをインポートして使用

- **ビューの追加**:
  1. `front/src/js/views/`に新しいビューファイルを作成
  2. ルーターに新しいルートを追加

- **スタイルの追加**:
  1. `front/src/css/`にスタイルを追加
  2. SCSSを使用する場合は`main.scss`に追加

## 使用方法

1. アプリケーションにアクセス: `http://localhost:3000`
2. ログインまたは新規ユーザー登録
3. ホームページでYouTubeビデオを検索
4. 検索結果から興味のあるビデオを選択
5. 「要約を生成」ボタンをクリックして要約を取得
6. プロフィールページでユーザー情報を管理
7. 認証テストページで認証状態とトークンを確認可能

## プロジェクト構造

```
プロジェクトルート/
├── backend/                  # バックエンドアプリケーション
│   ├── controllers/          # Blueprintコントローラー
│   │   ├── __init__.py
│   │   ├── auth_controller.py
│   │   ├── main_controller.py
│   │   └── profile_controller.py
│   ├── models/               # データモデル
│   │   └── user_profile.py
│   ├── services/             # サービスクラス
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   └── db_service.py
│   ├── app.py                # メインFlaskアプリケーション
│   ├── requirements.txt      # Pythonの依存関係
│   ├── setup.bat             # Windowsセットアップスクリプト
│   ├── setup.sh              # Unix/Linuxセットアップスクリプト
│   ├── test_api.py           # APIテスト
│   ├── test_auth.py          # 認証テスト
│   └── .env.example          # 環境変数のサンプル
│
├── front/                    # フロントエンドアプリケーション
│   ├── src/
│   │   ├── css/              # スタイルシート
│   │   │   ├── main.scss     # メインSCSSファイル
│   │   │   └── style.css     # カスタムスタイル
│   │   ├── js/               # JavaScriptファイル
│   │   │   ├── components/   # 再利用可能なコンポーネント
│   │   │   ├── services/     # APIサービス
│   │   │   │   ├── auth-api-service.js
│   │   │   │   ├── firebase.js
│   │   │   │   └── profile-api-service.js
│   │   │   ├── utils/        # ユーティリティ関数
│   │   │   │   └── auth-test.js
│   │   │   ├── views/        # ページビュー
│   │   │   │   ├── about.js
│   │   │   │   ├── auth-test.js
│   │   │   │   ├── contact.js
│   │   │   │   ├── home.js
│   │   │   │   ├── login.js
│   │   │   │   ├── profile.js
│   │   │   │   └── register.js
│   │   │   ├── bootstrap.js  # Bootstrap初期化
│   │   │   └── main.js       # メインエントリーポイント
│   ├── public/               # 静的ファイル
│   │   └── _redirects        # Netlify用リダイレクト設定
│   ├── etc/                  # その他の設定ファイル
│   ├── index.html            # メインHTMLファイル
│   ├── package.json          # npm依存関係
│   ├── vite.config.js        # Vite設定
│   └── .env.example          # 環境変数のサンプル
│
└── LICENSE                   # ライセンスファイル
```

## トラブルシューティング

### Firebase認証エラー

- **auth/configuration-not-found エラー**:
  1. `.env`ファイルが正しく設定されているか確認
  2. Firebase Consoleで認証機能が有効になっているか確認
  3. ブラウザのキャッシュとCookieをクリア
  4. 開発サーバーを再起動

- **トークン検証エラー**:
  1. バックエンドとフロントエンドのFirebase設定が同じプロジェクトを指しているか確認
  2. Firebase Admin SDKの秘密鍵が正しく設定されているか確認

### API接続エラー

- **CORS エラー**:
  1. バックエンドの`CORS_ORIGIN`設定がフロントエンドのURLと一致しているか確認
  2. フロントエンドの`VITE_API_BASE_URL`がバックエンドのURLと一致しているか確認

- **YouTube API エラー**:
  1. YouTube Data API v3が有効になっているか確認
  2. APIキーが正しく設定されているか確認
  3. APIキーの制限が適切に設定されているか確認

### Vertex AI エラー

- **Geminiモデルエラー**:
  1. Vertex AI APIが有効になっているか確認
  2. サービスアカウントに適切な権限があるか確認
  3. `GOOGLE_APPLICATION_CREDENTIALS`が正しく設定されているか確認

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は[LICENSE](LICENSE)ファイルを参照してください。
