"""
スキーマ検証モジュール
"""
from typing import Dict, Any, List, Optional, Union, Type
from marshmallow import Schema, fields, validate, ValidationError as MarshmallowValidationError
from errors import ValidationError


class BaseSchema(Schema):
    """基本スキーマクラス"""
    
    @classmethod
    def validate_request(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        リクエストデータを検証し、検証済みデータを返す
        
        Args:
            data: 検証するデータ
            
        Returns:
            検証済みデータ
            
        Raises:
            ValidationError: 検証エラーが発生した場合
        """
        try:
            return cls().load(data)
        except MarshmallowValidationError as e:
            raise ValidationError(
                message="入力データが無効です",
                payload={"errors": e.messages}
            )


class ProfileSchema(BaseSchema):
    """ユーザープロフィールスキーマ"""
    display_name = fields.String(
        validate=validate.Length(min=1, max=100),
        required=False,
        allow_none=True
    )
    bio = fields.String(
        validate=validate.Length(max=500),
        required=False,
        allow_none=True
    )
    location = fields.String(
        validate=validate.Length(max=100),
        required=False,
        allow_none=True
    )
    website = fields.String(
        validate=validate.Length(max=255),
        required=False,
        allow_none=True
    )


class SearchQuerySchema(BaseSchema):
    """検索クエリスキーマ"""
    q = fields.String(
        required=True,
        validate=validate.Length(min=1, max=100),
        error_messages={"required": "検索クエリは必須です"}
    )
    max_results = fields.Integer(
        required=False,
        validate=validate.Range(min=1, max=50),
        load_default=10
    )
