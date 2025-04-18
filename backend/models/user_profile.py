from services.db_service import db
from datetime import datetime

class UserProfile(db.Model):
    """
    ユーザープロフィールモデル
    
    ユーザーのプロフィール情報を保存するためのモデル。
    Firebase認証のユーザーIDと関連付けられます。
    """
    __tablename__ = 'user_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    firebase_uid = db.Column(db.String(128), unique=True, nullable=False)
    display_name = db.Column(db.String(100), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(100), nullable=True)
    website = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, firebase_uid, display_name=None, bio=None, location=None, website=None):
        self.firebase_uid = firebase_uid
        self.display_name = display_name
        self.bio = bio
        self.location = location
        self.website = website
    
    def to_dict(self):
        """プロフィールデータを辞書形式で返す"""
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
