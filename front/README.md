# YouTube検索・要約 フロントエンド

Firebase認証を使用し、YouTubeビデオを検索して要約を生成するシングルページアプリケーション（SPA）のフロントエンドです。バニラJavaScript、Bootstrap 5、Viteを使用して構築されています。

## 目次

- [機能概要](#機能概要)
- [技術スタック](#技術スタック)
- [セットアップ手順](#セットアップ手順)
  - [前提条件](#前提条件)
  - [インストール](#インストール)
  - [Firebase設定](#firebase設定)
  - [環境変数の設定](#環境変数の設定)
- [開発サーバーの起動](#開発サーバーの起動)
- [ビルドと本番デプロイ](#ビルドと本番デプロイ)
- [プロジェクト構造](#プロジェクト構造)
- [主要コンポーネント](#主要コンポーネント)
- [開発ガイド](#開発ガイド)
- [トラブルシューティング](#トラブルシューティング)

## 機能概要

このフロントエンドアプリケーションは以下の主要機能を提供します：

- **ユーザー認証**: Firebase Authenticationを使用したログイン・登録機能
- **YouTube検索**: キーワードに基づいてYouTubeビデオを検索
- **ビデオ要約**: 選択したビデオの内容をVertex AI Geminiで要約
- **プロフィール管理**: ユーザープロフィール情報の表示と編集
- **レスポンシブUI**: モバイルデバイスにも対応したインターフェース

## 技術スタック

- **HTML/CSS/JavaScript**: 基本的なWeb技術
- **Bootstrap 5**: UIコンポーネントとレスポンシブデザイン
- **Vite**: モジュールバンドラー・開発サーバー
- **Firebase SDK**: 認証とIDトークン管理
- **SCSS**: スタイリングの拡張機能
- **Fetch API**: バックエンドとの通信

## セットアップ手順

### 前提条件

- Node.js 14以上
- npm または yarn
- バックエンドAPIサーバー（別リポジトリ）
- Firebaseプロジェクト

### インストール

1. リポジトリをクローンします
2. frontディレクトリに移動します
3. 依存関係をインストールします：

```bash
npm install
# または
yarn
```

### Firebase設定

1. [Firebase Console](https://console.firebase.google.com/)にアクセスします
2. 新しいプロジェクトを作成するか、既存のプロジェクトを選択します
3. Authentication機能を有効にし、Email/Passwordプロバイダーを有効にします
4. プロジェクト設定からWebアプリを追加し、Firebase設定情報を取得します

### 環境変数の設定

1. `.env.example`ファイルをコピーして`.env`ファイルを作成します：

```bash
cp .env.example .env
```

2. `.env`ファイルを編集し、Firebase設定情報とAPIのURLを追加します：

```
VITE_FIREBASE_API_KEY=あなたのapiKey
VITE_FIREBASE_AUTH_DOMAIN=あなたのauthDomain
VITE_FIREBASE_PROJECT_ID=あなたのprojectId
VITE_FIREBASE_STORAGE_BUCKET=あなたのstorageBucket
VITE_FIREBASE_MESSAGING_SENDER_ID=あなたのmessagingSenderId
VITE_FIREBASE_APP_ID=あなたのappId

VITE_API_BASE_URL=http://localhost:5000
```

## 開発サーバーの起動

開発サーバーを起動するには：

```bash
npm run dev
# または
yarn dev
```

アプリケーションは`http://localhost:3000`でアクセスできます。

## ビルドと本番デプロイ

本番用にアプリケーションをビルドするには：

```bash
npm run build
# または
yarn build
```

ビルドされたファイルは`dist`ディレクトリに出力されます。これらのファイルは任意のWebサーバーにデプロイできます。

### Netlifyへのデプロイ

このプロジェクトはNetlifyへの簡単なデプロイをサポートしています。`public/_redirects`ファイルがSPAのルーティングを適切に処理します。

1. Netlifyアカウントを作成します
2. 新しいサイトを作成し、GitHubリポジトリと連携します
3. ビルドコマンドを`npm run build`に設定します
4. 公開ディレクトリを`dist`に設定します
5. 環境変数を設定します（`.env`ファイルと同じ変数）

## プロジェクト構造

```
front/
├── .env                  # 環境変数（gitignoreされる）
├── .env.example          # 環境変数のサンプル
├── index.html            # エントリーポイント
├── vite.config.js        # Vite設定
├── package.json          # npm依存関係
├── public/               # 静的ファイル
│   └── _redirects        # Netlify用リダイレクト設定
├── etc/                  # その他の設定ファイル
├── src/
│   ├── css/              # スタイルシート
│   │   ├── main.scss     # メインSCSSファイル（Bootstrapをインポート）
│   │   └── style.css     # カスタムスタイル
│   ├── js/               # JavaScriptファイル
│   │   ├── bootstrap.js  # Bootstrap JS初期化
│   │   ├── main.js       # メインエントリーポイント
│   │   ├── components/   # 再利用可能なコンポーネント
│   │   ├── services/     # APIサービス
│   │   │   ├── auth-api-service.js  # 認証API
│   │   │   ├── firebase.js          # Firebase初期化
│   │   │   └── profile-api-service.js # プロフィールAPI
│   │   ├── utils/        # ユーティリティ関数
│   │   │   └── auth-test.js # 認証テスト用ユーティリティ
│   │   └── views/        # ページビュー
│   │       ├── about.js      # 「About」ページ
│   │       ├── auth-test.js  # 認証テストページ
│   │       ├── contact.js    # 「お問い合わせ」ページ
│   │       ├── home.js       # ホームページ
│   │       ├── login.js      # ログインページ
│   │       ├── profile.js    # プロフィールページ
│   │       └── register.js   # 登録ページ
```

## 主要コンポーネント

### 認証システム

`src/js/services/firebase.js`ファイルはFirebase認証を初期化し、以下の機能を提供します：

- ユーザー登録（メール/パスワード）
- ログイン/ログアウト
- 認証状態の監視
- IDトークンの取得（APIリクエスト用）

### ルーティングシステム

このSPAは簡易的なクライアントサイドルーティングを実装しています：

- URLハッシュに基づいてビューを切り替え
- 認証状態に基づいたルート保護
- ページ遷移時のアニメーション

### APIサービス

`src/js/services/`ディレクトリには、バックエンドAPIと通信するためのサービスが含まれています：

- `auth-api-service.js`: 認証関連のAPI呼び出し
- `profile-api-service.js`: プロフィール管理のAPI呼び出し

## 開発ガイド

### 新しいビューの追加

1. `src/js/views/`ディレクトリに新しいJSファイルを作成します：

```javascript
// src/js/views/new-view.js
export default function renderNewView(container) {
  container.innerHTML = `
    <div class="container mt-4">
      <h1>新しいページ</h1>
      <p>ここに内容を記述します。</p>
    </div>
  `;
  
  // イベントリスナーの追加
  const someButton = container.querySelector('#some-button');
  if (someButton) {
    someButton.addEventListener('click', handleClick);
  }
  
  function handleClick() {
    // クリックイベントの処理
    console.log('ボタンがクリックされました');
  }
}
```

2. `src/js/main.js`にルートを追加します：

```javascript
import renderNewView from './views/new-view.js';

// ルートの定義
const routes = {
  // 既存のルート
  '#/': renderHomeView,
  '#/login': renderLoginView,
  
  // 新しいルート
  '#/new-page': renderNewView
};
```

### 新しいAPIサービスの追加

1. `src/js/services/`ディレクトリに新しいJSファイルを作成します：

```javascript
// src/js/services/new-api-service.js
import { getIdToken } from './firebase.js';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export async function fetchSomeData(params) {
  try {
    const token = await getIdToken();
    const response = await fetch(`${API_BASE_URL}/api/some-endpoint`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(params)
    });
    
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error fetching data:', error);
    throw error;
  }
}
```

2. 必要なビューからサービスをインポートして使用します：

```javascript
import { fetchSomeData } from '../services/new-api-service.js';

// ビュー内で使用
async function handleSubmit() {
  try {
    const result = await fetchSomeData({ param1: 'value1' });
    // 結果を処理
  } catch (error) {
    // エラーを処理
  }
}
```

### スタイルのカスタマイズ

1. Bootstrap変数をカスタマイズするには、`src/css/main.scss`を編集します：

```scss
// Bootstrapの変数をオーバーライド
$primary: #3f51b5;
$secondary: #ff4081;

// Bootstrapをインポート
@import "bootstrap/scss/bootstrap";

// カスタムスタイル
.custom-container {
  padding: 2rem;
  background-color: #f8f9fa;
}
```

2. カスタムCSSを追加するには、`src/css/style.css`を編集します：

```css
.feature-card {
  transition: transform 0.3s ease;
  margin-bottom: 1.5rem;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.1);
}
```

## トラブルシューティング

### Firebase認証エラー

#### auth/configuration-not-found エラー

このエラーが発生する一般的な原因と解決策：

1. **環境変数が正しく設定されていない**
   - `.env`ファイルが正しい場所（プロジェクトのルートディレクトリ）にあることを確認
   - 環境変数名が`VITE_`で始まっていることを確認
   - 値が正しく設定されていることを確認（引用符なし）

2. **Firebase Authenticationが有効になっていない**
   - Firebase Consoleで認証機能が有効になっていることを確認
   - Email/Passwordプロバイダーが有効になっていることを確認

3. **ブラウザのキャッシュ/Cookieの問題**
   - ブラウザのキャッシュとCookieをクリア
   - シークレットモードで試す

4. **Firebase設定の問題**
   - Firebase Consoleで正しいプロジェクトを選択していることを確認
   - Webアプリが正しく登録されていることを確認

5. **開発サーバーの再起動**
   - 環境変数を変更した後は、開発サーバーを再起動する

#### その他の認証エラー

- **auth/email-already-in-use**: 登録時に既に使用されているメールアドレス
- **auth/invalid-email**: 無効なメールアドレス形式
- **auth/user-not-found**: ログイン時にユーザーが見つからない
- **auth/wrong-password**: パスワードが間違っている

### API接続エラー

1. **バックエンドサーバーが実行されていない**
   - バックエンドサーバーが起動していることを確認
   - `VITE_API_BASE_URL`が正しいURLを指していることを確認

2. **CORS設定の問題**
   - バックエンドのCORS設定がフロントエンドのオリジンを許可していることを確認

3. **認証トークンの問題**
   - ユーザーがログインしていることを確認
   - IDトークンが正しく取得されていることを確認

### コンソールでのデバッグ

ブラウザのコンソールで以下の情報を確認することで、問題を特定できます：

- 環境変数が正しく読み込まれているか
- Firebase初期化エラーメッセージ
- API呼び出しのエラーメッセージ
- ネットワークリクエストとレスポンス

```javascript
// 環境変数のデバッグ
console.log('API URL:', import.meta.env.VITE_API_BASE_URL);

// Firebaseのデバッグ
import { auth } from './services/firebase.js';
console.log('Firebase Auth:', auth);

// APIリクエストのデバッグ
fetch(`${import.meta.env.VITE_API_BASE_URL}/api/test`)
  .then(response => console.log('API Response:', response))
  .catch(error => console.error('API Error:', error));
