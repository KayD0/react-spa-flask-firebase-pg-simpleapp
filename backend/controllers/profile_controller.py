"""
プロフィールコントローラー
"""
from typing import Dict, Any, Optional, Tuple
from flask import Blueprint, request, jsonify, g
from services.auth_service import auth_required, get_user_id_from_token
from models.user_profile import UserProfile
from services.db_service import db, add_to_db, commit_changes
from errors import register_error_handlers, BadRequestError, NotFoundError, DatabaseError
from schemas import ProfileSchema
from logger import get_logger

# ロガーの取得
logger = get_logger(__name__)

# Blueprintを作成
profile_bp = Blueprint('profile_bp', __name__, url_prefix='/api')

# エラーハンドラーを登録
register_error_handlers(profile_bp)

@profile_bp.route('/profile', methods=['GET'])
@auth_required
def get_profile():
    """
    ユーザープロフィールを取得します。
    このエンドポイントはauth_requiredデコレータで保護されています。
    
    Returns:
        ユーザープロフィール情報を含むJSONレスポンス
    """
    # 認証されたユーザーIDを取得
    firebase_uid = get_user_id_from_token()
    
    logger.info(f"ユーザープロフィール取得リクエスト: {firebase_uid}")
    
    # ユーザープロフィールを検索
    profile = UserProfile.get_by_firebase_uid(firebase_uid)
    
    if profile:
        # プロフィールが存在する場合は返す
        logger.info(f"既存のプロフィールを返します: {firebase_uid}")
        return jsonify({
            'success': True,
            'profile': profile.to_dict()
        })
    else:
        # プロフィールが存在しない場合は新規作成
        logger.info(f"新しいプロフィールを作成します: {firebase_uid}")
        new_profile = UserProfile(firebase_uid=firebase_uid)
        
        if not add_to_db(new_profile):
            logger.error(f"プロフィール作成エラー: {firebase_uid}")
            raise DatabaseError("プロフィールの作成中にエラーが発生しました")
        
        return jsonify({
            'success': True,
            'profile': new_profile.to_dict(),
            'message': 'プロフィールが作成されました'
        })


@profile_bp.route('/profile', methods=['PUT'])
@auth_required
def update_profile():
    """
    ユーザープロフィールを更新します。
    このエンドポイントはauth_requiredデコレータで保護されています。
    
    Request JSON:
        display_name: 表示名（オプション）
        bio: 自己紹介（オプション）
        location: 場所（オプション）
        website: ウェブサイト（オプション）
    
    Returns:
        更新されたユーザープロフィール情報を含むJSONレスポンス
    """
    # 認証されたユーザーIDを取得
    firebase_uid = get_user_id_from_token()
    
    # リクエストボディからJSONデータを取得
    data = request.get_json()
    
    if not data:
        logger.warning(f"更新データなしのリクエスト: {firebase_uid}")
        raise BadRequestError("更新するデータがありません")
    
    # データを検証
    validated_data = ProfileSchema.validate_request(data)
    
    logger.info(f"プロフィール更新リクエスト: {firebase_uid}")
    
    # ユーザープロフィールを検索
    profile = UserProfile.get_by_firebase_uid(firebase_uid)
    
    if not profile:
        # プロフィールが存在しない場合は新規作成
        logger.info(f"更新のために新しいプロフィールを作成します: {firebase_uid}")
        profile = UserProfile(firebase_uid=firebase_uid)
        db.session.add(profile)
    
    # プロフィールを更新
    profile.update(validated_data)
    
    # 変更を保存
    if not commit_changes():
        logger.error(f"プロフィール更新エラー: {firebase_uid}")
        raise DatabaseError("プロフィールの更新中にエラーが発生しました")
    
    logger.info(f"プロフィールが更新されました: {firebase_uid}")
    
    return jsonify({
        'success': True,
        'profile': profile.to_dict(),
        'message': 'プロフィールが更新されました'
    })


@profile_bp.route('/profile', methods=['DELETE'])
@auth_required
def delete_profile():
    """
    ユーザープロフィールを削除します。
    このエンドポイントはauth_requiredデコレータで保護されています。
    
    Returns:
        削除結果を含むJSONレスポンス
    """
    # 認証されたユーザーIDを取得
    firebase_uid = get_user_id_from_token()
    
    logger.info(f"プロフィール削除リクエスト: {firebase_uid}")
    
    # ユーザープロフィールを検索
    profile = UserProfile.get_by_firebase_uid(firebase_uid)
    
    if not profile:
        logger.warning(f"削除するプロフィールが見つかりません: {firebase_uid}")
        raise NotFoundError("削除するプロフィールが見つかりません")
    
    # プロフィールを削除
    try:
        db.session.delete(profile)
        if not commit_changes():
            logger.error(f"プロフィール削除エラー: {firebase_uid}")
            raise DatabaseError("プロフィールの削除中にエラーが発生しました")
        
        logger.info(f"プロフィールが削除されました: {firebase_uid}")
        
        return jsonify({
            'success': True,
            'message': 'プロフィールが削除されました'
        })
    except Exception as e:
        logger.error(f"プロフィール削除中の例外: {str(e)}")
        db.session.rollback()
        raise DatabaseError("プロフィールの削除中にエラーが発生しました")
