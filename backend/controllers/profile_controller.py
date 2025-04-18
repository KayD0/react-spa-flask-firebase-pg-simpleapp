from flask import Blueprint, request, jsonify
from services.auth_service import auth_required, get_user_id_from_token
from models.user_profile import UserProfile
from services.db_service import db

# Blueprintを作成
profile_bp = Blueprint('profile_bp', __name__, url_prefix='/api')

@profile_bp.route('/profile', methods=['GET'])
@auth_required
def get_profile():
    """
    ユーザープロフィールを取得します。
    このエンドポイントはauth_requiredデコレータで保護されています。
    
    戻り値:
    - ユーザープロフィール情報を含むJSONレスポンス
    """
    try:
        # 認証されたユーザーIDを取得
        firebase_uid = get_user_id_from_token()
        
        # ユーザープロフィールを検索
        profile = UserProfile.query.filter_by(firebase_uid=firebase_uid).first()
        
        if profile:
            # プロフィールが存在する場合は返す
            return jsonify({
                'success': True,
                'profile': profile.to_dict()
            })
        else:
            # プロフィールが存在しない場合は新規作成
            new_profile = UserProfile(firebase_uid=firebase_uid)
            db.session.add(new_profile)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'profile': new_profile.to_dict(),
                'message': 'プロフィールが作成されました'
            })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@profile_bp.route('/profile', methods=['PUT'])
@auth_required
def update_profile():
    """
    ユーザープロフィールを更新します。
    このエンドポイントはauth_requiredデコレータで保護されています。
    
    JSONボディパラメータ:
    - display_name: 表示名（オプション）
    - bio: 自己紹介（オプション）
    - location: 場所（オプション）
    - website: ウェブサイト（オプション）
    
    戻り値:
    - 更新されたユーザープロフィール情報を含むJSONレスポンス
    """
    try:
        # 認証されたユーザーIDを取得
        firebase_uid = get_user_id_from_token()
        
        # リクエストボディからJSONデータを取得
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': '更新するデータがありません'
            }), 400
        
        # ユーザープロフィールを検索
        profile = UserProfile.query.filter_by(firebase_uid=firebase_uid).first()
        
        if not profile:
            # プロフィールが存在しない場合は新規作成
            profile = UserProfile(firebase_uid=firebase_uid)
            db.session.add(profile)
        
        # 更新可能なフィールド
        updatable_fields = ['display_name', 'bio', 'location', 'website']
        
        # 提供されたフィールドを更新
        for field in updatable_fields:
            if field in data:
                setattr(profile, field, data[field])
        
        # 変更を保存
        db.session.commit()
        
        return jsonify({
            'success': True,
            'profile': profile.to_dict(),
            'message': 'プロフィールが更新されました'
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
