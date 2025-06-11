"""
APIエンドポイントのpytestによるテスト
"""
import json
from unittest.mock import patch, MagicMock

import pytest

from models.user_profile import UserProfile


def test_index_route(client):
    """インデックスルートのテスト"""
    response = client.get('/')
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data['status'] == 'running'
    assert 'message' in data
    assert 'endpoints' in data


class TestAuthRoutes:
    """認証ルートのテスト"""
    
    @patch('services.auth_service.verify_token')
    def test_verify_auth_success(self, mock_verify_token, client):
        """認証検証の成功テスト"""
        # モックの設定
        mock_user = {
            'uid': 'test-user-id',
            'email': 'test@example.com',
            'email_verified': True,
            'auth_time': 1600000000
        }
        mock_verify_token.return_value = mock_user
        
        # テスト
        response = client.post(
            '/api/auth/verify',
            headers={'Authorization': 'Bearer test-token'}
        )
        data = json.loads(response.data)
        
        assert response.status_code == 200
        assert data['authenticated'] is True
        assert data['user']['uid'] == 'test-user-id'
        assert data['user']['email'] == 'test@example.com'
    
    def test_verify_auth_no_token(self, client):
        """認証トークンなしのテスト"""
        response = client.post('/api/auth/verify')
        data = json.loads(response.data)
        
        assert response.status_code == 401
        assert data['error'] == 'unauthorized'
    
    @patch('services.auth_service.verify_token')
    def test_check_token_success(self, mock_verify_token, client):
        """トークン検証の成功テスト"""
        # モックの設定
        mock_user = {
            'uid': 'test-user-id',
            'email': 'test@example.com',
            'email_verified': True,
            'auth_time': 1600000000
        }
        mock_verify_token.return_value = mock_user
        
        # テスト
        response = client.post(
            '/api/auth/token',
            json={'token': 'test-token'}
        )
        data = json.loads(response.data)
        
        assert response.status_code == 200
        assert data['valid'] is True
        assert data['user']['uid'] == 'test-user-id'
    
    def test_check_token_no_token(self, client):
        """トークンなしのテスト"""
        response = client.post('/api/auth/token', json={})
        data = json.loads(response.data)
        
        assert response.status_code == 401
        assert data['error'] == 'unauthorized'


class TestProfileRoutes:
    """プロフィールルートのテスト"""
    
    @patch('services.auth_service.get_user_id_from_token')
    def test_get_profile_new_user(self, mock_get_user_id, client, auth_headers):
        """新規ユーザーのプロフィール取得テスト"""
        # モックの設定
        mock_get_user_id.return_value = 'test-user-id'
        
        # テスト
        response = client.get('/api/profile', headers=auth_headers)
        data = json.loads(response.data)
        
        assert response.status_code == 200
        assert data['success'] is True
        assert data['profile']['firebase_uid'] == 'test-user-id'
        assert 'message' in data
    
    @patch('services.auth_service.get_user_id_from_token')
    def test_get_profile_existing_user(self, mock_get_user_id, client, auth_headers, create_test_profile):
        """既存ユーザーのプロフィール取得テスト"""
        # モックの設定
        mock_get_user_id.return_value = 'test-user-id'
        
        # テスト用のプロフィールを作成
        create_test_profile()
        
        # テスト
        response = client.get('/api/profile', headers=auth_headers)
        data = json.loads(response.data)
        
        assert response.status_code == 200
        assert data['success'] is True
        assert data['profile']['firebase_uid'] == 'test-user-id'
        assert data['profile']['display_name'] == 'Test User'
        assert data['profile']['bio'] == 'Test bio'
    
    @patch('services.auth_service.get_user_id_from_token')
    def test_update_profile_new_user(self, mock_get_user_id, client, auth_headers):
        """新規ユーザーのプロフィール更新テスト"""
        # モックの設定
        mock_get_user_id.return_value = 'test-user-id'
        
        # テスト
        response = client.put(
            '/api/profile',
            headers=auth_headers,
            json={
                'display_name': 'Updated Name',
                'bio': 'Updated bio',
                'location': 'Tokyo',
                'website': 'https://example.com'
            }
        )
        data = json.loads(response.data)
        
        assert response.status_code == 200
        assert data['success'] is True
        assert data['profile']['firebase_uid'] == 'test-user-id'
        assert data['profile']['display_name'] == 'Updated Name'
        assert data['profile']['bio'] == 'Updated bio'
        assert data['profile']['location'] == 'Tokyo'
        assert data['profile']['website'] == 'https://example.com'
    
    @patch('services.auth_service.get_user_id_from_token')
    def test_update_profile_existing_user(self, mock_get_user_id, client, auth_headers, create_test_profile):
        """既存ユーザーのプロフィール更新テスト"""
        # モックの設定
        mock_get_user_id.return_value = 'test-user-id'
        
        # テスト用のプロフィールを作成
        create_test_profile()
        
        # テスト
        response = client.put(
            '/api/profile',
            headers=auth_headers,
            json={
                'display_name': 'Updated Name',
                'location': 'Tokyo'
            }
        )
        data = json.loads(response.data)
        
        assert response.status_code == 200
        assert data['success'] is True
        assert data['profile']['firebase_uid'] == 'test-user-id'
        assert data['profile']['display_name'] == 'Updated Name'
        assert data['profile']['bio'] == 'Test bio'  # 更新されていないフィールド
        assert data['profile']['location'] == 'Tokyo'
    
    @patch('services.auth_service.get_user_id_from_token')
    def test_delete_profile(self, mock_get_user_id, client, auth_headers, create_test_profile, app):
        """プロフィール削除テスト"""
        # モックの設定
        mock_get_user_id.return_value = 'test-user-id'
        
        # テスト用のプロフィールを作成
        create_test_profile()
        
        # テスト
        response = client.delete('/api/profile', headers=auth_headers)
        data = json.loads(response.data)
        
        assert response.status_code == 200
        assert data['success'] is True
        assert 'message' in data
        
        # プロフィールが削除されたことを確認
        profile = UserProfile.query.filter_by(firebase_uid='test-user-id').first()
        assert profile is None
    
    @patch('services.auth_service.get_user_id_from_token')
    def test_delete_profile_not_found(self, mock_get_user_id, client, auth_headers):
        """存在しないプロフィールの削除テスト"""
        # モックの設定
        mock_get_user_id.return_value = 'test-user-id'
        
        # テスト
        response = client.delete('/api/profile', headers=auth_headers)
        data = json.loads(response.data)
        
        assert response.status_code == 404
        assert data['error'] == 'not_found'
