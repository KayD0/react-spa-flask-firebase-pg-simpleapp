# YouTube検索・要約アプリケーション

YouTubeビデオを検索し、AI駆動の要約を生成するフルスタックアプリケーションです。React SPAフロントエンド、Flaskバックエンド、PostgreSQLデータベースを使用し、Firebase認証とVertex AI Geminiモデルを統合しています。

![アプリケーションイメージ]()

## 目次

- [機能概要](#機能概要)
- [技術スタック](#技術スタック)
- [アーキテクチャ](#アーキテクチャ)
- [セットアップ手順](#セットアップ手順)
  - [前提条件](#前提条件)
  - [バックエンドのセットアップ](#バックエンドのセットアップ)
  - [フロントエンドのセットアップ](#フロントエンドのセットアップ)
  - [APIキーの取得](#apiキーの取得)
- [アプリケーションの実行](#アプリケーションの実行)
- [主要機能の使い方](#主要機能の使い方)
- [開発ガイド](#開発ガイド)
- [デプロイ](#デプロイ)
- [トラブルシューティング](#トラブルシューティング)
- [ライセンス](#ライセンス)

## 機能概要

このアプリケーションは以下の主要機能を提供します：

- **ユーザー認証**: Firebase Authenticationを使用したログイン・登録機能
- **プロフィール管理**: ユーザープロフィール情報の保存と取得
- **レスポンシブUI**: モバイルデバイスにも対応したインターフェース

## 技術スタック

### フロントエンド
- **React**: UIコンポーネントとステート管理
- **Vite**: 高速な開発環境とビルドツール
- **Bootstrap 5**: レスポンシブデザインとUIコンポーネント
- **Firebase SDK**: クライアントサイド認証

### バックエンド
- **Python 3.7+**: サーバーサイド言語
- **Flask**: Webフレームワーク
- **Blueprint**: モジュール化されたルーティング
- **Firebase Admin SDK**: IDトークン検証
- **YouTube Data API v3**: ビデオ検索と情報取得
- **Vertex AI Gemini**: AI要約生成

### データベース
- **PostgreSQL**: ユーザープロフィールとアプリケーションデータの永続化

## アーキテクチャ
- **フロントエンド**: ユーザーインターフェースを提供し、バックエンドAPIと通信
- **バックエンド**: ビジネスロジックを処理し、外部APIと通信
- **データベース**: ユーザーデータと検索履歴を保存
- **外部サービス**: 認証、ビデオ検索、AI要約生成を提供

## セットアップ手順

### 前提条件

- Node.js 14以上
- Python 3.7以上
- PostgreSQL 12以上
- Google Cloud Platform アカウント
- Firebase プロジェクト

### バックエンドのセットアップ

1. backendディレクトリに移動します
2. 仮想環境を作成して有効化します：

```bash
# 仮想環境の作成
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. 必要な依存関係をインストールします：

```bash
pip install -r requirements.txt
```

4. `.env.example`ファイルを基に`.env`ファイルを作成します：

```bash
cp .env.example .env
```

5. `.env`ファイルを編集し、APIキーと設定を追加します（詳細は[APIキーの取得](#apiキーの取得)セクションを参照）

### フロントエンドのセットアップ

1. frontディレクトリに移動します
2. 依存関係をインストールします：

```bash
npm install
# または
yarn
```

3. `.env.example`ファイルをコピーして`.env`ファイルを作成します：

```bash
cp .env.example .env
```

4. `.env`ファイルを編集し、Firebase設定情報とAPIのURLを追加します（詳細は[APIキーの取得](#apiキーの取得)セクションを参照）

### APIキーの取得

#### Firebase認証のセットアップ

1. [Firebase Console](https://console.firebase.google.com/)にアクセスします
2. 新しいプロジェクトを作成するか、既存のプロジェクトを選択します
3. Authentication機能を有効化し、メール/パスワード認証を設定します
4. プロジェクト設定からWebアプリを追加し、Firebase設定情報を取得します
5. Firebase設定情報をフロントエンドの`.env`ファイルにコピーします
6. プロジェクト設定 > サービスアカウントに移動します
7. 「新しい秘密鍵を生成」をクリックしてJSONファイルをダウンロードします
8. JSONファイルの内容をバックエンドの`.env`ファイルの対応する変数に設定します

#### PostgreSQLのセットアップ

1. PostgreSQLをインストールし、新しいデータベースを作成します
2. データベース接続情報をバックエンドの`.env`ファイルに追加します：

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=youtube_summary
DB_USER=postgres
DB_PASSWORD=yourpassword
```

## アプリケーションの実行

### バックエンドの起動

backendディレクトリで以下のコマンドを実行します：

```bash
# Windows
setup.bat

# macOS/Linux
./setup.sh

# または直接実行
python app.py
```

バックエンドサーバーは`http://localhost:5000`で起動します。

### フロントエンドの起動

frontディレクトリで以下のコマンドを実行します：

```bash
npm run dev
# または
yarn dev
```

フロントエンドアプリケーションは`http://localhost:3000`でアクセスできます。

## 主要機能の使い方

### ユーザー登録とログイン

1. アプリケーションにアクセスし、「登録」ボタンをクリックします
2. メールアドレスとパスワードを入力して新しいアカウントを作成します
3. 登録後、自動的にログインされます
4. 次回からは「ログイン」ページでメールアドレスとパスワードを入力してログインできます

### プロフィール管理

1. 画面右上のユーザーアイコンをクリックし、「プロフィール」を選択します
2. プロフィール情報（表示名、設定など）を表示・編集できます
3. 変更後、「保存」ボタンをクリックして更新します

## 開発ガイド

### プロジェクト構造

```
react-spa-flask-postgres-app/
├── LICENSE
├── README.md
├── backend/               # Flaskバックエンド
│   ├── .env.example       # 環境変数のサンプル
│   ├── app.py             # アプリケーションのエントリーポイント
│   ├── requirements.txt   # Python依存関係
│   ├── setup.bat          # Windowsセットアップスクリプト
│   ├── setup.sh           # Unix/Linuxセットアップスクリプト
│   ├── controllers/       # ルートハンドラー
│   ├── models/            # データモデル
│   └── services/          # ビジネスロジック
├── front/                 # Reactフロントエンド
    ├── .env.example       # 環境変数のサンプル
    ├── index.html         # HTMLエントリーポイント
    ├── package.json       # npm依存関係
    ├── vite.config.js     # Vite設定
    ├── public/            # 静的ファイル
    └── src/               # ソースコード
        ├── App.jsx        # メインアプリコンポーネント
        ├── main.jsx       # Reactエントリーポイント
        ├── components/    # 再利用可能なコンポーネント
        ├── contexts/      # Reactコンテキスト
        ├── css/           # スタイルシート
        ├── js/            # JavaScriptユーティリティ
        ├── pages/         # ページコンポーネント
        └── services/      # APIサービス
```

### バックエンド開発

新しいエンドポイントを追加するには：

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

### フロントエンド開発

新しいページを追加するには：

1. `src/pages/`ディレクトリに新しいJSXファイルを作成します
2. 必要なコンポーネントとサービスをインポートします
3. ページコンポーネントを実装します
4. `App.jsx`にルートを追加します

## デプロイ

### バックエンドのデプロイ

バックエンドはHeroku、Google Cloud Run、AWS Elastic Beanstalkなどのサービスにデプロイできます。

例：Herokuへのデプロイ

1. Herokuアカウントを作成し、Heroku CLIをインストールします
2. backendディレクトリに`Procfile`を作成します：

```
web: gunicorn app:app
```

3. 依存関係に`gunicorn`を追加します
4. Herokuアプリを作成し、デプロイします：

```bash
heroku create
git push heroku main
```

5. 環境変数を設定します：

```bash
heroku config:set YOUTUBE_API_KEY=your_api_key
# その他の環境変数も同様に設定
```

### フロントエンドのデプロイ

フロントエンドはNetlify、Vercel、GitHub Pagesなどのサービスにデプロイできます。

例：Netlifyへのデプロイ

1. frontディレクトリでアプリケーションをビルドします：

```bash
npm run build
```

2. Netlifyアカウントを作成します
3. Netlify CLIをインストールします：

```bash
npm install -g netlify-cli
```

4. デプロイします：

```bash
netlify deploy --prod
```

5. 環境変数を設定します（Netlifyダッシュボードから）

## トラブルシューティング

### 一般的な問題と解決策

#### バックエンド接続エラー

- バックエンドサーバーが実行されていることを確認
- CORSが正しく設定されていることを確認
- 環境変数`VITE_API_BASE_URL`が正しいURLを指していることを確認

#### 認証エラー

- Firebase設定が正しいことを確認
- バックエンドとフロントエンドが同じFirebaseプロジェクトを使用していることを確認
- IDトークンが正しく取得・検証されていることを確認

### ログの確認

問題のトラブルシューティングには、ログを確認することが役立ちます：

- **バックエンド**: デバッグモードで実行
  ```bash
  python app.py --debug
  ```

- **フロントエンド**: ブラウザのコンソールでエラーを確認

## ライセンス

このプロジェクトは[MITライセンス](LICENSE)の下で公開されています。
