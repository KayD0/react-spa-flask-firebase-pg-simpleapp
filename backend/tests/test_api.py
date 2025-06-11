"""
APIエンドポイントのユニットテスト
"""
import os
import sys
import unittest
import json
from unittest.mock import patch, MagicMock

# テスト対象のアプリケーションをインポートできるようにパスを追加
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from services.db_service import db
from models.user_profile import UserProfile


class BaseTestCase(unittest.TestCase):
    """テストケースの基底クラス"""
    
    def setUp(self):
        """各テストの前に実行"""
        # テスト用の設定でアプリケーションを作成
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['WTF_CSRF_ENABLED'] = False
        
        # テスト用のクライアントを作成
        self.client = self.app.test_client()
        
        # アプリケーションコンテキストを設定
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # テスト用のデータベースを作成
        db.create_all()
    
    def tearDown(self):
        """各テストの後に実行"""
        # テスト用のデータベースをクリア
        db.session.remove()
        db.drop_all()
        
        # アプリケーションコンテキストを解放
        self.app_context.pop()


class MainRoutesTestCase(BaseTestCase):
    """メインルートのテスト"""
    
    def test_index_route(self):
        """インデックスルートのテスト"""
        response = self.client.get('/')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'running')
        self.assertIn('message', data)
        self.assertIn('endpoints', data)


class AuthRoutesTestCase(BaseTestCase):
    """認証ルートのテスト"""
    
    @patch('services.auth_service.verify_token')
    def test_verify_auth_success(self, mock_verify_token):
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
        response = self.client.post(
            '/api/auth/verify',
            headers={'Authorization': 'Bearer test-token'}
        )
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['authenticated'])
        self.assertEqual(data['user']['uid'], 'test-user-id')
        self.assertEqual(data['user']['email'], 'test@example.com')
    
    def test_verify_auth_no_token(self):
        """認証トークンなしのテスト"""
        response = self.client.post('/api/auth/verify')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['error'], 'unauthorized')
    
    @patch('services.auth_service.verify_token')
    def test_check_token_success(self, mock_verify_token):
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
        response = self.client.post(
            '/api/auth/token',
            json={'token': 'test-token'}
        )
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['valid'])
        self.assertEqual(data['user']['uid'], 'test-user-id')
    
    def test_check_token_no_token(self):
        """トークンなしのテスト"""
        response = self.client.post('/api/auth/token', json={})
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['error'], 'unauthorized')


class ProfileRoutesTestCase(BaseTestCase):
    """プロフィールルートのテスト"""
    
    @patch('services.auth_service.get_user_id_from_token')
    def test_get_profile_new_user(self, mock_get_user_id):
        """新規ユーザーのプロフィール取得テスト"""
        # モックの設定
        mock_get_user_id.return_value = 'test-user-id'
        
        # テスト
        response = self.client.get(
            '/api/profile',
            headers={'Authorization': 'Bearer test-token'}
        )
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['profile']['firebase_uid'], 'test-user-id')
        self.assertIn('message', data)
    
    @patch('services.auth_service.get_user_id_from_token')
    def test_get_profile_existing_user(self, mock_get_user_id):
        """既存ユーザーのプロフィール取得テスト"""
        # モックの設定
        mock_get_user_id.return_value = 'test-user-id'
        
        # テスト用のプロフィールを作成
        profile = UserProfile(
            firebase_uid='test-user-id',
            display_name='Test User',
            bio='Test bio'
        )
        db.session.add(profile)
        db.session.commit()
        
        # テスト
        response = self.client.get(
            '/api/profile',
            headers={'Authorization': 'Bearer test-token'}
        )
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['profile']['firebase_uid'], 'test-user-id')
        self.assertEqual(data['profile']['display_name'], 'Test User')
        self.assertEqual(data['profile']['bio'], 'Test bio')
    
    @patch('services.auth_service.get_user_id_from_token')
    def test_update_profile_new_user(self, mock_get_user_id):
        """新規ユーザーのプロフィール更新テスト"""
        # モックの設定
        mock_get_user_id.return_value = 'test-user-id'
        
        # テスト
        response = self.client.put(
            '/api/profile',
            headers={'Authorization': 'Bearer test-token'},
            json={
                'display_name': 'Updated Name',
                'bio': 'Updated bio',
                'location': 'Tokyo',
                'website': 'https://example.com'
            }
        )
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['profile']['firebase_uid'], 'test-user-id')
        self.assertEqual(data['profile']['display_name'], 'Updated Name')
        self.assertEqual(data['profile']['bio'], 'Updated bio')
        self.assertEqual(data['profile']['location'], 'Tokyo')
        self.assertEqual(data['profile']['website'], 'https://example.com')
    
    @patch('services.auth_service.get_user_id_from_token')
    def test_update_profile_existing_user(self, mock_get_user_id):
        """既存ユーザーのプロフィール更新テスト"""
        # モックの設定
        mock_get_user_id.return_value = 'test-user-id'
        
        # テスト用のプロフィールを作成
        profile = UserProfile(
            firebase_uid='test-user-id',
            display_name='Test User',
            bio='Test bio'
        )
        db.session.add(profile)
        db.session.commit()
        
        # テスト
        response = self.client.put(
            '/api/profile',
            headers={'Authorization': 'Bearer test-token'},
            json={
                'display_name': 'Updated Name',
                'location': 'Tokyo'
            }
        )
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['profile']['firebase_uid'], 'test-user-id')
        self.assertEqual(data['profile']['display_name'], 'Updated Name')
        self.assertEqual(data['profile']['bio'], 'Test bio')  # 更新されていないフィールド
        self.assertEqual(data['profile']['location'], 'Tokyo')
    
    @patch('services.auth_service.get_user_id_from_token')
    def test_delete_profile(self, mock_get_user_id):
        """プロフィール削除テスト"""
        # モックの設定
        mock_get_user_id.return_value = 'test-user-id'
        
        # テスト用のプロフィールを作成
        profile = UserProfile(
            firebase_uid='test-user-id',
            display_name='Test User'
        )
        db.session.add(profile)
        db.session.commit()
        
        # テスト
        response = self.client.delete(
            '/api/profile',
            headers={'Authorization': 'Bearer test-token'}
        )
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('message', data)
        
        # プロフィールが削除されたことを確認
        profile = UserProfile.query.filter_by(firebase_uid='test-user-id').first()
        self.assertIsNone(profile)
    
    @patch('services.auth_service.get_user_id_from_token')
    def test_delete_profile_not_found(self, mock_get_user_id):
        """存在しないプロフィールの削除テスト"""
        # モックの設定
        mock_get_user_id.return_value = 'test-user-id'
        
        # テスト
        response = self.client.delete(
            '/api/profile',
            headers={'Authorization': 'Bearer test-token'}
        )
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['error'], 'not_found')


if __name__ == '__main__':
    unittest.main()
