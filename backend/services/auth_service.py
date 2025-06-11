"""
Firebase認証サービスモジュール - IDトークンの検証用
"""
import os
from typing import Dict, Any, Optional, Callable
import firebase_admin
from firebase_admin import credentials, auth
from functools import wraps
from flask import request, current_app, g
from errors import UnauthorizedError, ForbiddenError, ExternalServiceError
from logger import get_logger

# ロガーの取得
logger = get_logger(__name__)

def initialize_firebase() -> bool:
    """
    環境変数からの認証情報を使用してFirebase Admin SDKを初期化する
    
    Returns:
        bool: 初期化が成功したかどうか
    """
    try:
        # 既に初期化されているかチェック
        if not firebase_admin._apps:
            # 設定からFirebase認証情報を取得
            config = current_app.config
            
            # Firebase認証情報が設定されているかチェック
            if config.get('FIREBASE_PROJECT_ID'):
                cred_dict = {
                    "type": "service_account",
                    "project_id": config.get('FIREBASE_PROJECT_ID'),
                    "private_key_id": config.get('FIREBASE_PRIVATE_KEY_ID'),
                    "private_key": config.get('FIREBASE_PRIVATE_KEY', '').replace('\\n', '\n'),
                    "client_email": config.get('FIREBASE_CLIENT_EMAIL'),
                    "client_id": config.get('FIREBASE_CLIENT_ID'),
                    "auth_uri": config.get('FIREBASE_AUTH_URI'),
                    "token_uri": config.get('FIREBASE_TOKEN_URI'),
                    "auth_provider_x509_cert_url": config.get('FIREBASE_AUTH_PROVIDER_X509_CERT_URL'),
                    "client_x509_cert_url": config.get('FIREBASE_CLIENT_X509_CERT_URL')
                }
                cred = credentials.Certificate(cred_dict)
                firebase_admin.initialize_app(cred)
                logger.info("Firebase Admin SDKがサービスアカウント認証情報で初期化されました")
            else:
                # サービスアカウントが提供されていない場合はアプリケーションのデフォルト認証情報を使用
                firebase_admin.initialize_app()
                logger.info("Firebase Admin SDKがアプリケーションのデフォルト認証情報で初期化されました")
            return True
    except Exception as e:
        logger.error(f"Firebase Admin SDKの初期化エラー: {str(e)}")
        return False


def auth_required(f: Callable) -> Callable:
    """
    Firebase認証を必要とするFlaskルートのためのデコレータ。
    AuthorizationヘッダーのIDトークンを検証し、デコードされたトークンをリクエストに追加します。
    
    Args:
        f: デコレートする関数
        
    Returns:
        デコレートされた関数
    """
    @wraps(f)
    def decorated_function(*args: Any, **kwargs: Any) -> Any:
        # リクエストヘッダーから認証トークンを取得
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            logger.warning("認証ヘッダーがありません")
            raise UnauthorizedError("Authorizationヘッダーがありません")
        
        # トークンを抽出（'Bearer 'プレフィックスがある場合は削除）
        token = auth_header.replace('Bearer ', '') if auth_header.startswith('Bearer ') else auth_header
        
        try:
            # トークンを検証
            decoded_token = auth.verify_id_token(token)
            
            # デコードされたトークンをリクエストオブジェクトとFlask gオブジェクトに追加
            request.user = decoded_token
            g.user = decoded_token
            g.user_id = decoded_token.get('uid')
            
            logger.info(f"ユーザー認証成功: {g.user_id}")
            
            # ルート関数を続行
            return f(*args, **kwargs)
        except auth.InvalidIdTokenError:
            logger.warning("無効な認証トークン")
            raise UnauthorizedError("無効な認証トークンです")
        except auth.ExpiredIdTokenError:
            logger.warning("期限切れの認証トークン")
            raise UnauthorizedError("期限切れの認証トークンです")
        except auth.RevokedIdTokenError:
            logger.warning("取り消された認証トークン")
            raise UnauthorizedError("取り消された認証トークンです")
        except auth.CertificateFetchError:
            logger.error("Firebase証明書の取得エラー")
            raise ExternalServiceError("認証サービスとの通信中にエラーが発生しました")
        except Exception as e:
            logger.error(f"認証エラー: {str(e)}")
            raise UnauthorizedError(f"認証エラー: {str(e)}")
    
    return decorated_function


def verify_token(token: str) -> Dict[str, Any]:
    """
    Firebase IDトークンを検証し、有効な場合はデコードされたトークンを返します。
    
    Args:
        token: 検証するFirebase IDトークン
        
    Returns:
        デコードされたトークン
        
    Raises:
        UnauthorizedError: トークンが無効な場合
        ExternalServiceError: 外部サービスとの通信エラーの場合
    """
    try:
        return auth.verify_id_token(token)
    except auth.InvalidIdTokenError:
        logger.warning("無効な認証トークン")
        raise UnauthorizedError("無効な認証トークンです")
    except auth.ExpiredIdTokenError:
        logger.warning("期限切れの認証トークン")
        raise UnauthorizedError("期限切れの認証トークンです")
    except auth.RevokedIdTokenError:
        logger.warning("取り消された認証トークン")
        raise UnauthorizedError("取り消された認証トークンです")
    except auth.CertificateFetchError:
        logger.error("Firebase証明書の取得エラー")
        raise ExternalServiceError("認証サービスとの通信中にエラーが発生しました")
    except Exception as e:
        logger.error(f"認証エラー: {str(e)}")
        raise UnauthorizedError(f"認証エラー: {str(e)}")


def get_user_id_from_token() -> str:
    """
    現在のリクエストのトークンからユーザーIDを取得します。
    auth_requiredデコレータが適用されたルート内で使用することを想定しています。
    
    Returns:
        ユーザーID
        
    Raises:
        UnauthorizedError: ユーザーが認証されていない場合
    """
    if hasattr(g, 'user_id'):
        return g.user_id
    
    if not hasattr(request, 'user'):
        logger.warning("認証されていないリクエストでユーザーIDが要求されました")
        raise UnauthorizedError('認証されていません。auth_requiredデコレータを使用してください。')
    
    user_id = request.user.get('uid')
    if not user_id:
        logger.warning("ユーザートークンにUIDがありません")
        raise UnauthorizedError('ユーザーIDが見つかりません')
    
    return user_id


def require_role(role: str) -> Callable:
    """
    特定のロールを持つユーザーのみがアクセスできるようにするデコレータ
    
    Args:
        role: 必要なロール
        
    Returns:
        デコレータ関数
    """
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def decorated_function(*args: Any, **kwargs: Any) -> Any:
            # auth_requiredデコレータが先に適用されていることを前提とする
            if not hasattr(request, 'user'):
                logger.warning("認証されていないリクエストでロールチェックが要求されました")
                raise UnauthorizedError('認証されていません')
            
            # ユーザーのロールをチェック
            user_roles = request.user.get('roles', [])
            if role not in user_roles:
                logger.warning(f"ユーザーに必要なロール '{role}' がありません")
                raise ForbiddenError(f"このアクションには '{role}' ロールが必要です")
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator
