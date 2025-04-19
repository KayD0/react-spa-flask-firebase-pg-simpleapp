# React SPA フロントエンド

Firebase認証を使用したシングルページアプリケーション（SPA）のフロントエンドです。React、Vite、Bootstrap 5を使用して構築されています。

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
- **プロフィール管理**: ユーザープロフィール情報の表示と編集
- **レスポンシブUI**: モバイルデバイスにも対応したインターフェース

## 技術スタック

- **React**: UIライブラリ
- **JSX**: コンポーネント記述言語
- **Bootstrap 5**: UIコンポーネントとレスポンシブデザイン
- **Vite**: モジュールバンドラー・開発サーバー
- **Firebase SDK**: 認証とIDトークン管理
- **SCSS**: スタイリングの拡張機能
- **Fetch API**: バックエンドとの通信

## セットアップ手順

### 前提条件

- Node.js 14以上
- npm または yarn
- Goバックエンドサーバー（別ディレクトリ）
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

VITE_API_BASE_URL=http://localhost:8080
```

## 開発サーバーの起動

開発サーバーを起動するには：

```bash
npm run dev
# または
yarn dev
```

アプリケーションは`http://localhost:5173`でアクセスできます。

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
├── package-lock.json     # npm依存関係ロック
├── public/               # 静的ファイル
│   └── _redirects        # Netlify用リダイレクト設定
├── etc/                  # その他の設定ファイル
├── src/
│   ├── components/       # 再利用可能なコンポーネント
│   │   └── NavBar.jsx    # ナビゲーションバー
│   ├── contexts/         # Reactコンテキスト
│   │   └── AuthContext.jsx # 認証コンテキスト
│   ├── css/              # スタイルシート
│   │   ├── main.scss     # メインSCSSファイル（Bootstrapをインポート）
│   │   └── style.css     # カスタムスタイル
│   ├── js/               # JavaScriptファイル
│   │   ├── bootstrap.js  # Bootstrap JS初期化
│   │   ├── main.js       # メインJavaScriptファイル
│   │   ├── services/     # APIサービス
│   │   │   ├── auth-api-service.js  # 認証API
│   │   │   ├── firebase.js          # Firebase初期化
│   │   │   └── profile-api-service.js # プロフィールAPI
│   │   └── utils/        # ユーティリティ関数
│   │       └── auth-test.js # 認証テスト用ユーティリティ
│   ├── pages/            # ページコンポーネント
│   │   ├── AboutPage.jsx     # 「About」ページ
│   │   ├── AuthTestPage.jsx  # 認証テストページ
│   │   ├── ContactPage.jsx   # 「お問い合わせ」ページ
│   │   ├── HomePage.jsx      # ホームページ
│   │   ├── LoginPage.jsx     # ログインページ
│   │   ├── ProfilePage.jsx   # プロフィールページ
│   │   └── RegisterPage.jsx  # 登録ページ
│   ├── services/         # サービス
│   │   └── api.js        # API通信
│   ├── App.jsx           # メインReactコンポーネント
│   └── main.jsx          # Reactエントリーポイント
```

## 主要コンポーネント

### 認証システム

`src/contexts/AuthContext.jsx`ファイルはFirebase認証を初期化し、以下の機能を提供します：

- ユーザー登録（メール/パスワード）
- ログイン/ログアウト
- 認証状態の監視
- IDトークンの取得（APIリクエスト用）

### ルーティングシステム

このSPAはReactベースのルーティングを実装しています：

- URLパスに基づいてコンポーネントを切り替え
- 認証状態に基づいたルート保護
- ページ遷移時のアニメーション

### APIサービス

`src/js/services/`ディレクトリには、バックエンドAPIと通信するためのサービスが含まれています：

- `auth-api-service.js`: 認証関連のAPI呼び出し
- `profile-api-service.js`: プロフィール管理のAPI呼び出し

## 開発ガイド

### 新しいページの追加

1. `src/pages/`ディレクトリに新しいJSXファイルを作成します：

```jsx
// src/pages/NewPage.jsx
import React, { useState } from 'react';

const NewPage = () => {
  const [data, setData] = useState('');
  
  const handleClick = () => {
    setData('ボタンがクリックされました');
  };
  
  return (
    <div className="container mt-4">
      <h1>新しいページ</h1>
      <p>ここに内容を記述します。</p>
      <button 
        className="btn btn-primary" 
        onClick={handleClick}
      >
        クリック
      </button>
      {data && <p className="mt-3">{data}</p>}
    </div>
  );
};

export default NewPage;
```

2. `src/App.jsx`にルートを追加します：

```jsx
import NewPage from './pages/NewPage';

// App.jsxのルーティング部分
<Routes>
  {/* 既存のルート */}
  <Route path="/" element={<HomePage />} />
  <Route path="/login" element={<LoginPage />} />
  
  {/* 新しいルート */}
  <Route path="/new-page" element={<NewPage />} />
</Routes>
```

### 新しいコンポーネントの追加

1. `src/components/`ディレクトリに新しいJSXファイルを作成します：

```jsx
// src/components/CustomCard.jsx
import React from 'react';

const CustomCard = ({ title, content, imageUrl }) => {
  return (
    <div className="card mb-4">
      {imageUrl && (
        <img src={imageUrl} className="card-img-top" alt={title} />
      )}
      <div className="card-body">
        <h5 className="card-title">{title}</h5>
        <p className="card-text">{content}</p>
      </div>
    </div>
  );
};

export default CustomCard;
```

2. 他のコンポーネントやページからインポートして使用します：

```jsx
import CustomCard from '../components/CustomCard';

// ページコンポーネント内で使用
<div className="row">
  <div className="col-md-4">
    <CustomCard 
      title="カード1" 
      content="これはカード1の内容です。" 
      imageUrl="/images/card1.jpg" 
    />
  </div>
  <div className="col-md-4">
    <CustomCard 
      title="カード2" 
      content="これはカード2の内容です。" 
    />
  </div>
</div>
```

### 新しいAPIサービスの追加

1. `src/services/`ディレクトリに新しいJSファイルを作成します：

```javascript
// src/services/new-api-service.js
import { getIdToken } from '../js/services/firebase';

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

2. Reactコンポーネントからサービスをインポートして使用します：

```jsx
import React, { useState, useEffect } from 'react';
import { fetchSomeData } from '../services/new-api-service';

const DataComponent = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  const loadData = async () => {
    setLoading(true);
    try {
      const result = await fetchSomeData({ param1: 'value1' });
      setData(result);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };
  
  useEffect(() => {
    loadData();
  }, []);
  
  return (
    <div className="container">
      {loading && <p>読み込み中...</p>}
      {error && <p className="text-danger">エラー: {error}</p>}
      {data && (
        <div>
          <h2>データ</h2>
          <pre>{JSON.stringify(data, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default DataComponent;
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
   - `VITE_API_BASE_URL`が正しいURLを指していることを確認（`http://localhost:8080`）

2. **CORS設定の問題**
   - バックエンドのCORS設定がフロントエンドのオリジン（`http://localhost:5173`）を許可していることを確認

3. **認証トークンの問題**
   - ユーザーがログインしていることを確認
   - IDトークンが正しく取得されていることを確認

### Reactコンポーネントのデバッグ

Reactコンポーネントのデバッグには以下の方法が有効です：

1. **React Developer Tools**
   - Chromeまたは他のブラウザ用のReact Developer Tools拡張機能をインストール
   - コンポーネントツリーとprops/stateを検査

2. **console.log**
   - コンポーネントのレンダリングやライフサイクルをデバッグ
   ```jsx
   useEffect(() => {
     console.log('Component mounted with props:', props);
     return () => console.log('Component unmounted');
   }, [props]);
   ```

3. **エラーバウンダリ**
   - エラーバウンダリコンポーネントを作成してエラーをキャッチ
   ```jsx
   class ErrorBoundary extends React.Component {
     state = { hasError: false, error: null };
     
     static getDerivedStateFromError(error) {
       return { hasError: true, error };
     }
     
     render() {
       if (this.state.hasError) {
         return <div>エラーが発生しました: {this.state.error.message}</div>;
       }
       return this.props.children;
     }
   }
