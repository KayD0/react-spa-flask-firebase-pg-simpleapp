"""
データベースサービスモジュール
"""
from typing import Any, Optional, List, Dict, Type
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from logger import get_logger

# ロガーの取得
logger = get_logger(__name__)

# SQLAlchemyインスタンスを作成
db = SQLAlchemy()

def init_db(app: Flask) -> None:
    """
    Flaskアプリケーションにデータベース設定を適用し、SQLAlchemyを初期化します。
    
    Args:
        app: Flaskアプリケーションインスタンス
    """
    # 設定はすでにapp.configに適用されているため、
    # ここではSQLAlchemyの初期化のみを行う
    db.init_app(app)
    logger.info("データベース接続が初期化されました")

def commit_changes() -> bool:
    """
    データベースの変更をコミットする
    
    Returns:
        bool: コミットが成功したかどうか
    """
    try:
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        logger.error(f"データベースコミットエラー: {str(e)}")
        return False

def add_to_db(model_instance: Any) -> bool:
    """
    モデルインスタンスをデータベースに追加する
    
    Args:
        model_instance: 追加するモデルインスタンス
        
    Returns:
        bool: 追加が成功したかどうか
    """
    try:
        db.session.add(model_instance)
        return commit_changes()
    except Exception as e:
        logger.error(f"データベース追加エラー: {str(e)}")
        return False

def delete_from_db(model_instance: Any) -> bool:
    """
    モデルインスタンスをデータベースから削除する
    
    Args:
        model_instance: 削除するモデルインスタンス
        
    Returns:
        bool: 削除が成功したかどうか
    """
    try:
        db.session.delete(model_instance)
        return commit_changes()
    except Exception as e:
        logger.error(f"データベース削除エラー: {str(e)}")
        return False
