"""
データベースセットアップスクリプト

このスクリプトはデータベースの作成とマイグレーションを行います。
アプリケーション起動とは別に実行することで、データベースの初期化と
マイグレーションを分離します。
"""
import os
import sys
import argparse
from flask import Flask
from dotenv import load_dotenv

# 設定のインポート
from config import get_config

# サービスのインポート
from services.db_service import init_db, db

# ロギングのインポート
from logger import setup_logger, get_logger

# ロガーの取得
logger = get_logger(__name__)

def create_app_for_db():
    """
    データベース操作用のFlaskアプリケーションを作成
    
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
    
    # データベースの初期化
    init_db(app)
    
    return app

def create_tables(app, drop_all=False):
    """
    データベーステーブルを作成
    
    Args:
        app: Flaskアプリケーションインスタンス
        drop_all: 既存のテーブルを削除するかどうか
    """
    with app.app_context():
        if drop_all:
            logger.info("既存のデータベーステーブルを削除します...")
            db.drop_all()
            logger.info("データベーステーブルが削除されました")
        
        logger.info("データベーステーブルを作成します...")
        db.create_all()
        logger.info("データベーステーブルが作成されました")

def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(description='データベースセットアップツール')
    parser.add_argument('--drop', action='store_true', help='既存のテーブルを削除して再作成')
    parser.add_argument('--env', type=str, default='development', 
                        help='環境設定 (development, testing, production)')
    
    args = parser.parse_args()
    
    # 環境変数の設定
    os.environ['FLASK_ENV'] = args.env
    
    # アプリケーションの作成
    app = create_app_for_db()
    
    # データベーステーブルの作成
    create_tables(app, args.drop)
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
