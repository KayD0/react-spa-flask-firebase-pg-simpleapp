"""
メインコントローラー
"""
from flask import Blueprint, jsonify, current_app
from errors import register_error_handlers
from logger import get_logger

# ロガーの取得
logger = get_logger(__name__)

# Blueprintを作成
main_bp = Blueprint('main_bp', __name__)

# エラーハンドラーを登録
register_error_handlers(main_bp)

@main_bp.route('/')
def index():
    """
    APIが実行中であることを確認するための簡単なインデックスルート。
    
    Returns:
        APIの状態と利用可能なエンドポイントの情報を含むJSONレスポンス
    """
    logger.info("インデックスエンドポイントにアクセスされました")
    
    # アプリケーションのバージョン情報（設定から取得）
    version = current_app.config.get('VERSION', '1.0.0')
    
    return jsonify({
        'status': 'running',
        'version': version,
        'message': 'ユーザープロフィールAPIが実行中です',
        'endpoints': {
            'auth_verify': '/api/auth/verify (Authorizationヘッダーを持つPOST)',
            'profile_get': '/api/profile (Authorizationヘッダーを持つGET)',
            'profile_update': '/api/profile (JSONボディとAuthorizationヘッダーを持つPUT)'
        }
    })
