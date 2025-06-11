"""
エラーハンドリングモジュール
"""
from typing import Dict, Any, Optional, Type, Union
from flask import jsonify, Blueprint
from werkzeug.exceptions import HTTPException


class APIError(Exception):
    """API例外の基底クラス"""
    status_code = 500
    error_code = "internal_error"
    message = "内部サーバーエラーが発生しました"
    
    def __init__(
        self, 
        message: Optional[str] = None, 
        status_code: Optional[int] = None,
        error_code: Optional[str] = None,
        payload: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message or self.message)
        self.message = message or self.message
        self.status_code = status_code or self.status_code
        self.error_code = error_code or self.error_code
        self.payload = payload or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """エラーレスポンス用の辞書を返す"""
        error_dict = {
            'error': self.error_code,
            'message': self.message,
            'status_code': self.status_code
        }
        if self.payload:
            error_dict['details'] = self.payload
        return error_dict


class BadRequestError(APIError):
    """不正なリクエストエラー"""
    status_code = 400
    error_code = "bad_request"
    message = "リクエストが不正です"


class UnauthorizedError(APIError):
    """認証エラー"""
    status_code = 401
    error_code = "unauthorized"
    message = "認証が必要です"


class ForbiddenError(APIError):
    """権限エラー"""
    status_code = 403
    error_code = "forbidden"
    message = "このリソースにアクセスする権限がありません"


class NotFoundError(APIError):
    """リソースが見つからないエラー"""
    status_code = 404
    error_code = "not_found"
    message = "指定されたリソースが見つかりません"


class ValidationError(APIError):
    """入力検証エラー"""
    status_code = 422
    error_code = "validation_error"
    message = "入力データが無効です"


class RateLimitError(APIError):
    """レート制限エラー"""
    status_code = 429
    error_code = "rate_limit_exceeded"
    message = "リクエスト制限を超えました。しばらく待ってから再試行してください"


class DatabaseError(APIError):
    """データベースエラー"""
    status_code = 500
    error_code = "database_error"
    message = "データベース操作中にエラーが発生しました"


class ExternalServiceError(APIError):
    """外部サービスエラー"""
    status_code = 502
    error_code = "external_service_error"
    message = "外部サービスとの通信中にエラーが発生しました"


# エラーハンドラーを登録するための関数
def register_error_handlers(app_or_blueprint: Union[Blueprint, Any]) -> None:
    """
    アプリケーションまたはBlueprintにエラーハンドラーを登録する
    
    Args:
        app_or_blueprint: エラーハンドラーを登録するFlaskアプリケーションまたはBlueprint
    """
    @app_or_blueprint.errorhandler(APIError)
    def handle_api_error(error: APIError):
        """APIエラーハンドラー"""
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response
    
    @app_or_blueprint.errorhandler(HTTPException)
    def handle_http_exception(error: HTTPException):
        """HTTPException（Werkzeug例外）ハンドラー"""
        response = jsonify({
            'error': error.name.lower().replace(' ', '_'),
            'message': error.description,
            'status_code': error.code
        })
        response.status_code = error.code
        return response
    
    @app_or_blueprint.errorhandler(Exception)
    def handle_generic_exception(error: Exception):
        """一般的な例外ハンドラー"""
        # 本番環境では詳細なエラーメッセージを表示しないようにすべき
        response = jsonify({
            'error': 'internal_error',
            'message': '内部サーバーエラーが発生しました',
            'status_code': 500
        })
        response.status_code = 500
        return response
