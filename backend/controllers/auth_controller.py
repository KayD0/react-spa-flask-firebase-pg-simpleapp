"""
認証コントローラー
"""
from flask import Blueprint, request, jsonify, g
from services.auth_service import auth_required, verify_token
from errors import register_error_handlers, UnauthorizedError
from logger import get_logger

# ロガーの取得
logger = get_logger(__name__)

# Blueprintを作成
auth_bp = Blueprint('auth_bp', __name__, url_prefix='/api/auth')

# エラーハンドラーを登録
register_error_handlers(auth_bp)

@auth_bp.route('/verify', methods=['POST'])
@auth_required
def verify_auth():
    """
    認証トークンを検証し、ユーザー情報を返します。
    このエンドポイントはauth_requiredデコレータで保護されています。
    
    Returns:
        デコードされたトークンからのユーザー情報を含むJSONレスポンス
    """
    # auth_requiredデコレータがデコードされたトークンをrequest.userとg.userに追加します
    user_info = g.user
    
    logger.info(f"ユーザー認証が検証されました: {user_info.get('uid')}")
    
    # ユーザー情報を返す
    return jsonify({
        'authenticated': True,
        'user': {
            'uid': user_info.get('uid'),
            'email': user_info.get('email'),
            'email_verified': user_info.get('email_verified', False),
            'auth_time': user_info.get('auth_time')
        }
    })

@auth_bp.route('/token', methods=['POST'])
def check_token():
    """
    トークンを検証し、有効かどうかを返します。
    auth_requiredデコレータを使用せずに、トークンの検証のみを行います。
    
    Request JSON:
        token: 検証するFirebase IDトークン
    
    Returns:
        トークンの検証結果を含むJSONレスポンス
    """
    data = request.get_json()
    
    if not data or 'token' not in data:
        logger.warning("トークンが提供されていません")
        raise UnauthorizedError("トークンが必要です")
    
    token = data['token']
    
    # トークンを検証
    decoded_token = verify_token(token)
    
    logger.info(f"トークンが検証されました: {decoded_token.get('uid')}")
    
    return jsonify({
        'valid': True,
        'user': {
            'uid': decoded_token.get('uid'),
            'email': decoded_token.get('email'),
            'email_verified': decoded_token.get('email_verified', False),
            'auth_time': decoded_token.get('auth_time')
        }
    })
