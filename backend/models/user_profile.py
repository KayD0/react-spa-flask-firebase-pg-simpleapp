"""
ユーザープロフィールモデル
"""
from typing import Dict, Any, Optional
from datetime import datetime
from services.db_service import db


class UserProfile(db.Model):
    """
    ユーザープロフィールモデル
    
    ユーザーのプロフィール情報を保存するためのモデル。
    Firebase認証のユーザーIDと関連付けられます。
    """
    __tablename__ = 'user_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    firebase_uid = db.Column(db.String(128), unique=True, nullable=False, index=True)
    display_name = db.Column(db.String(100), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(100), nullable=True)
    website = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(
        self, 
        firebase_uid: str, 
        display_name: Optional[str] = None, 
        bio: Optional[str] = None, 
        location: Optional[str] = None, 
        website: Optional[str] = None
    ) -> None:
        """
        ユーザープロフィールの初期化
        
        Args:
            firebase_uid: Firebase認証のユーザーID
            display_name: 表示名（オプション）
            bio: 自己紹介（オプション）
            location: 場所（オプション）
            website: ウェブサイト（オプション）
        """
        self.firebase_uid = firebase_uid
        self.display_name = display_name
        self.bio = bio
        self.location = location
        self.website = website
    
    def to_dict(self) -> Dict[str, Any]:
        """
        プロフィールデータを辞書形式で返す
        
        Returns:
            プロフィールデータの辞書
        """
        return {
            'id': self.id,
            'firebase_uid': self.firebase_uid,
            'display_name': self.display_name,
            'bio': self.bio,
            'location': self.location,
            'website': self.website,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def get_by_firebase_uid(cls, firebase_uid: str) -> Optional['UserProfile']:
        """
        Firebase UIDでユーザープロフィールを取得する
        
        Args:
            firebase_uid: Firebase認証のユーザーID
            
        Returns:
            ユーザープロフィールまたはNone
        """
        return cls.query.filter_by(firebase_uid=firebase_uid).first()
    
    def update(self, data: Dict[str, Any]) -> None:
        """
        プロフィールデータを更新する
        
        Args:
            data: 更新するデータの辞書
        """
        # 更新可能なフィールド
        updatable_fields = ['display_name', 'bio', 'location', 'website']
        
        # 提供されたフィールドを更新
        for field in updatable_fields:
            if field in data:
                setattr(self, field, data[field])
