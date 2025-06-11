"""
アプリケーション設定モジュール
"""
import os
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

class Config:
    """基本設定クラス"""
    # アプリケーション設定
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-please-change-in-production')
    
    # データベース設定
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        f"postgresql+psycopg://{os.getenv('DB_USER', 'postgres')}:"
        f"{os.getenv('DB_PASSWORD', 'postgres')}@"
        f"{os.getenv('DB_HOST', 'localhost')}:"
        f"{os.getenv('DB_PORT', '5432')}/"
        f"{os.getenv('DB_NAME', 'youtubeapp')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # CORS設定
    CORS_ORIGIN = os.getenv('CORS_ORIGIN', 'http://localhost:3000')
    
    # Firebase設定
    FIREBASE_PROJECT_ID = os.getenv('FIREBASE_PROJECT_ID')
    FIREBASE_PRIVATE_KEY_ID = os.getenv('FIREBASE_PRIVATE_KEY_ID')
    FIREBASE_PRIVATE_KEY = os.getenv('FIREBASE_PRIVATE_KEY')
    FIREBASE_CLIENT_EMAIL = os.getenv('FIREBASE_CLIENT_EMAIL')
    FIREBASE_CLIENT_ID = os.getenv('FIREBASE_CLIENT_ID')
    FIREBASE_AUTH_URI = os.getenv('FIREBASE_AUTH_URI', 'https://accounts.google.com/o/oauth2/auth')
    FIREBASE_TOKEN_URI = os.getenv('FIREBASE_TOKEN_URI', 'https://oauth2.googleapis.com/token')
    FIREBASE_AUTH_PROVIDER_X509_CERT_URL = os.getenv('FIREBASE_AUTH_PROVIDER_X509_CERT_URL', 'https://www.googleapis.com/oauth2/v1/certs')
    FIREBASE_CLIENT_X509_CERT_URL = os.getenv('FIREBASE_CLIENT_X509_CERT_URL')


class DevelopmentConfig(Config):
    """開発環境設定"""
    DEBUG = True
    

class TestingConfig(Config):
    """テスト環境設定"""
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class ProductionConfig(Config):
    """本番環境設定"""
    # 本番環境では必ず強力な秘密鍵を設定すること
    SECRET_KEY = os.getenv('SECRET_KEY')
    
    # 本番環境では必ずSSLを使用すること
    # SESSION_COOKIE_SECURE = True
    # REMEMBER_COOKIE_SECURE = True


# 環境に基づいて設定を選択
config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

# 現在の環境を取得（デフォルトは開発環境）
def get_config():
    """現在の環境に基づいて設定を返す"""
    env = os.getenv('FLASK_ENV', 'development')
    return config_by_name.get(env, config_by_name['default'])
