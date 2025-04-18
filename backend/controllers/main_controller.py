from flask import Blueprint, jsonify

# Blueprintを作成
main_bp = Blueprint('main_bp', __name__)

@main_bp.route('/')
def index():
    """APIが実行中であることを確認するための簡単なインデックスルート。"""
    return jsonify({
        'message': 'ユーザープロフィールAPIが実行中です',
        'endpoints': {
            'auth_verify': '/api/auth/verify (Authorizationヘッダーを持つPOST)',
            'profile_get': '/api/profile/ (Authorizationヘッダーを持つGET)',
            'profile_update': '/api/profile/ (JSONボディとAuthorizationヘッダーを持つPUT)'
        }
    })
