import React, { useState, useEffect } from 'react';
import { Card, Form, Button, Alert, Row, Col, ListGroup } from 'react-bootstrap';
import { useAuth } from '../contexts/AuthContext';
import { getProfile, updateProfile } from '../services/api';

const ProfilePage = () => {
  const { currentUser } = useAuth();
  const [profileData, setProfileData] = useState({
    display_name: '',
    bio: '',
    location: '',
    website: ''
  });
  const [isLoading, setIsLoading] = useState(true);
  const [isEditing, setIsEditing] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [alert, setAlert] = useState({
    show: false,
    variant: 'success',
    message: ''
  });

  // Fetch profile data on component mount
  useEffect(() => {
    const fetchProfileData = async () => {
      try {
        setIsLoading(true);
        const result = await getProfile();
        
        if (result.success) {
          setProfileData({
            display_name: result.profile.display_name || '',
            bio: result.profile.bio || '',
            location: result.profile.location || '',
            website: result.profile.website || ''
          });
        }
      } catch (error) {
        console.error('Error fetching profile:', error);
        setAlert({
          show: true,
          variant: 'danger',
          message: 'プロフィール情報の取得に失敗しました。'
        });
      } finally {
        setIsLoading(false);
      }
    };

    fetchProfileData();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setProfileData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSave = async () => {
    try {
      setIsSaving(true);
      const result = await updateProfile(profileData);
      
      if (result.success) {
        setAlert({
          show: true,
          variant: 'success',
          message: 'プロフィールが更新されました'
        });
        setIsEditing(false);
        
        // Auto-hide alert after 3 seconds
        setTimeout(() => {
          setAlert(prev => ({ ...prev, show: false }));
        }, 3000);
      }
    } catch (error) {
      console.error('Error updating profile:', error);
      setAlert({
        show: true,
        variant: 'danger',
        message: `エラー: ${error.message || 'プロフィールの更新に失敗しました'}`
      });
    } finally {
      setIsSaving(false);
    }
  };

  if (isLoading) {
    return (
      <div className="text-center my-5">
        <div className="spinner-border" role="status">
          <span className="visually-hidden">読み込み中...</span>
        </div>
        <p className="mt-2">プロフィール情報を読み込んでいます...</p>
      </div>
    );
  }

  return (
    <Row>
      <Col md={8}>
        <Card className="mb-4">
          <Card.Header>
            <h2 className="card-title mb-0">ユーザープロフィール</h2>
          </Card.Header>
          
          {/* Alert */}
          {alert.show && (
            <Alert 
              variant={alert.variant} 
              className="m-3"
              dismissible
              onClose={() => setAlert(prev => ({ ...prev, show: false }))}
            >
              {alert.message}
            </Alert>
          )}
          
          {/* Profile Info Display */}
          {!isEditing ? (
            <Card.Body id="profileInfo">
              <div className="mb-4">
                <h4>{profileData.display_name || currentUser.email}</h4>
                <p><strong>メールアドレス:</strong> {currentUser.email}</p>
                
                {profileData.bio && (
                  <div className="mb-2">
                    <p><strong>自己紹介:</strong> {profileData.bio}</p>
                  </div>
                )}
                
                {profileData.location && (
                  <div className="mb-2">
                    <p><strong>場所:</strong> {profileData.location}</p>
                  </div>
                )}
                
                {profileData.website && (
                  <div className="mb-2">
                    <p>
                      <strong>ウェブサイト:</strong>{' '}
                      <a 
                        href={profileData.website.startsWith('http') ? profileData.website : `https://${profileData.website}`} 
                        target="_blank" 
                        rel="noopener noreferrer"
                      >
                        {profileData.website}
                      </a>
                    </p>
                  </div>
                )}
              </div>
              
              <div className="d-flex">
                <Button 
                  variant="primary" 
                  onClick={() => setIsEditing(true)}
                >
                  プロフィール編集
                </Button>
              </div>
            </Card.Body>
          ) : (
            /* Profile Edit Form */
            <Card.Body id="profileForm">
              <Form>
                <Form.Group className="mb-3" controlId="displayName">
                  <Form.Label>表示名</Form.Label>
                  <Form.Control
                    type="text"
                    name="display_name"
                    value={profileData.display_name}
                    onChange={handleChange}
                    placeholder="表示名を入力"
                  />
                </Form.Group>
                
                <Form.Group className="mb-3" controlId="bio">
                  <Form.Label>自己紹介</Form.Label>
                  <Form.Control
                    as="textarea"
                    rows={3}
                    name="bio"
                    value={profileData.bio}
                    onChange={handleChange}
                    placeholder="自己紹介を入力"
                  />
                </Form.Group>
                
                <Form.Group className="mb-3" controlId="location">
                  <Form.Label>場所</Form.Label>
                  <Form.Control
                    type="text"
                    name="location"
                    value={profileData.location}
                    onChange={handleChange}
                    placeholder="場所を入力"
                  />
                </Form.Group>
                
                <Form.Group className="mb-3" controlId="website">
                  <Form.Label>ウェブサイト</Form.Label>
                  <Form.Control
                    type="text"
                    name="website"
                    value={profileData.website}
                    onChange={handleChange}
                    placeholder="ウェブサイトを入力"
                  />
                </Form.Group>
                
                <div className="d-flex">
                  <Button
                    variant="success"
                    className="me-2"
                    onClick={handleSave}
                    disabled={isSaving}
                  >
                    {isSaving ? (
                      <>
                        <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                        保存中...
                      </>
                    ) : '保存'}
                  </Button>
                  <Button
                    variant="secondary"
                    onClick={() => setIsEditing(false)}
                  >
                    キャンセル
                  </Button>
                </div>
              </Form>
            </Card.Body>
          )}
        </Card>
      </Col>
      
      <Col md={4}>
        <Card className="bg-light">
          <Card.Header>
            <h5 className="card-title mb-0">アカウント設定</h5>
          </Card.Header>
          <ListGroup variant="flush">
            <ListGroup.Item action>パスワード変更</ListGroup.Item>
            <ListGroup.Item action disabled>プライバシー設定</ListGroup.Item>
          </ListGroup>
        </Card>
      </Col>
    </Row>
  );
};

export default ProfilePage;
