"""
Pytest設定ファイル - テスト用のフィクスチャとヘルパー関数を定義
"""
import os
import sys
import pytest
from flask import Flask

# テスト対象のアプリケーションをインポートできるようにパスを追加
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from services.db_service import db
from models.user_profile import UserProfile


@pytest.fixture
def app():
    """テスト用のFlaskアプリケーションを作成するフィクスチャ"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    
    # アプリケーションコンテキストを設定
    with app.app_context():
        # テスト用のデータベースを作成
        db.create_all()
        yield app
        # テスト用のデータベースをクリア
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """テスト用のクライアントを作成するフィクスチャ"""
    return app.test_client()


@pytest.fixture
def runner(app):
    """テスト用のCLIランナーを作成するフィクスチャ"""
    return app.test_cli_runner()


@pytest.fixture
def auth_headers():
    """認証ヘッダーを作成するフィクスチャ"""
    return {'Authorization': 'Bearer test-token'}


@pytest.fixture
def create_test_profile(app):
    """テスト用のユーザープロフィールを作成するフィクスチャ"""
    def _create_profile(firebase_uid='test-user-id', display_name='Test User', bio='Test bio'):
        profile = UserProfile(
            firebase_uid=firebase_uid,
            display_name=display_name,
            bio=bio
        )
        db.session.add(profile)
        db.session.commit()
        return profile
    
    return _create_profile
