"""
アプリケーションのエントリーポイント
"""
import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

# 設定のインポート
from config import get_config

# サービスのインポート
from services.auth_service import initialize_firebase
from services.db_service import init_db, db

# コントローラー（Blueprint）のインポート
from controllers.main_controller import main_bp
from controllers.auth_controller import auth_bp
from controllers.profile_controller import profile_bp

# エラーハンドリングのインポート
from errors import register_error_handlers

# ロギングのインポート
from logger import setup_logger, get_logger

# ロガーの取得
logger = get_logger(__name__)

def create_app(config_name=None):
    """
    アプリケーションファクトリー関数
    
    Args:
        config_name: 設定名（development, testing, production）
        
    Returns:
        設定済みのFlaskアプリケーションインスタンス
    """
    # 環境変数の読み込み
    load_dotenv()
    
    # Flaskアプリケーションの作成
    app = Flask(__name__)
    
    # 設定の適用
    config_obj = get_config()
    app.config.from_object(config_obj)
    
    # ロガーの設定
    setup_logger(app)
    
    # CORSの設定
    CORS(app, resources={r"/api/*": {"origins": app.config['CORS_ORIGIN']}})
    
    # グローバルエラーハンドラーの登録
    register_error_handlers(app)
    
    # データベースの初期化
    init_db(app)
    
    # Blueprintの登録
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)
    
    # アプリケーションコンテキスト内でのセットアップ
    with app.app_context():
        # Firebase Admin SDKの初期化
        firebase_initialized = initialize_firebase()
        if not firebase_initialized:
            logger.warning("Firebase Admin SDKの初期化に失敗しました")
        
        # アプリケーションの起動ログ
        logger.info(f"アプリケーションが起動しました（環境: {os.getenv('FLASK_ENV', 'development')}）")
    
    return app

# アプリケーションのインスタンスを作成
app = create_app()

if __name__ == '__main__':
    # Flaskアプリを実行
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
