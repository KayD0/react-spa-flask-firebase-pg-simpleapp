"""
Firebase認証検証のためのpytestによる統合テスト
"""
import os
import pytest
import requests
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

# APIベースURL
API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:5000')


@pytest.mark.integration
def test_auth_verification_no_token():
    """認証トークンなしでの認証検証エンドポイントのテスト"""
    response = requests.post(f"{API_BASE_URL}/api/auth/verify")
    
    assert response.status_code in [401, 403], "未認証アクセスは401または403を返すべき"
    data = response.json()
    assert 'error' in data, "エラーメッセージが含まれるべき"


@pytest.mark.integration
def test_auth_verification_invalid_token():
    """無効なトークンでの認証検証エンドポイントのテスト"""
    headers = {"Authorization": "Bearer invalid_token"}
    response = requests.post(f"{API_BASE_URL}/api/auth/verify", headers=headers)
    
    assert response.status_code in [401, 403], "無効なトークンは401または403を返すべき"
    data = response.json()
    assert 'error' in data, "エラーメッセージが含まれるべき"


@pytest.mark.integration
@pytest.mark.skipif(not os.getenv('FIREBASE_ID_TOKEN'), reason="FIREBASE_ID_TOKEN環境変数が設定されていません")
def test_auth_verification_valid_token():
    """有効なトークンでの認証検証エンドポイントのテスト"""
    token = os.getenv('FIREBASE_ID_TOKEN')
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{API_BASE_URL}/api/auth/verify", headers=headers)
    
    assert response.status_code == 200, "有効なトークンは200を返すべき"
    data = response.json()
    assert data.get('authenticated') is True, "認証成功を示すべき"
    assert 'user' in data, "ユーザー情報が含まれるべき"


@pytest.mark.integration
@pytest.mark.skipif(not os.getenv('FIREBASE_ID_TOKEN'), reason="FIREBASE_ID_TOKEN環境変数が設定されていません")
def test_search_endpoint_with_auth():
    """認証付きでの検索エンドポイントのテスト"""
    token = os.getenv('FIREBASE_ID_TOKEN')
    headers = {"Authorization": f"Bearer {token}"}
    
    search_data = {
        "q": "python プログラミング",
        "max_results": 5
    }
    
    response = requests.post(
        f"{API_BASE_URL}/api/search", 
        headers=headers,
        json=search_data
    )
    
    assert response.status_code == 200, "認証付きの検索リクエストは200を返すべき"
    data = response.json()
    assert 'videos' in data, "検索結果にはビデオ情報が含まれるべき"
