import React, { useState } from 'react';
import { Card, Button, Alert, Row, Col, Spinner } from 'react-bootstrap';
import { useAuth } from '../contexts/AuthContext';
import { verifyAuth } from '../services/api';

const AuthTestPage = () => {
  const { currentUser } = useAuth();
  const [verificationResult, setVerificationResult] = useState(null);
  const [isVerifying, setIsVerifying] = useState(false);
  const [error, setError] = useState('');

  const handleVerifyToken = async () => {
    setIsVerifying(true);
    setError('');
    setVerificationResult(null);

    try {
      const result = await verifyAuth();
      setVerificationResult(result);
    } catch (err) {
      console.error('Token verification error:', err);
      setError(err.message || '認証トークンの検証中にエラーが発生しました。');
    } finally {
      setIsVerifying(false);
    }
  };

  return (
    <>
      <Row className="mb-4">
        <Col>
          <Card>
            <Card.Body>
              <Card.Title as="h1">認証テスト</Card.Title>
              <Card.Text>
                このページでは、Firebase認証とバックエンドAPIの連携をテストできます。
                「トークンを検証」ボタンをクリックして、認証トークンがバックエンドで正しく検証されるか確認してください。
              </Card.Text>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      <Row>
        <Col md={6}>
          <Card className="mb-4">
            <Card.Header className="bg-primary text-white">
              <h5 className="mb-0">現在のユーザー情報</h5>
            </Card.Header>
            <Card.Body>
              {currentUser ? (
                <div>
                  <p><strong>UID:</strong> {currentUser.uid}</p>
                  <p><strong>メールアドレス:</strong> {currentUser.email}</p>
                  <p><strong>メール確認済み:</strong> {currentUser.emailVerified ? 'はい' : 'いいえ'}</p>
                  <p><strong>作成日時:</strong> {new Date(currentUser.metadata.creationTime).toLocaleString('ja-JP')}</p>
                  <p><strong>最終ログイン:</strong> {new Date(currentUser.metadata.lastSignInTime).toLocaleString('ja-JP')}</p>
                </div>
              ) : (
                <p>ユーザー情報を読み込み中...</p>
              )}
            </Card.Body>
          </Card>
        </Col>

        <Col md={6}>
          <Card className="mb-4">
            <Card.Header className="bg-info text-white">
              <h5 className="mb-0">認証トークン検証</h5>
            </Card.Header>
            <Card.Body>
              {error && (
                <Alert variant="danger" dismissible onClose={() => setError('')}>
                  {error}
                </Alert>
              )}

              <div className="d-grid gap-2">
                <Button 
                  variant="primary" 
                  onClick={handleVerifyToken}
                  disabled={isVerifying}
                >
                  {isVerifying ? (
                    <>
                      <Spinner animation="border" size="sm" className="me-2" />
                      検証中...
                    </>
                  ) : 'トークンを検証'}
                </Button>
              </div>

              {verificationResult && (
                <div className="mt-4">
                  <h6>検証結果:</h6>
                  <Alert variant="success">
                    <p><strong>成功:</strong> {verificationResult.success ? 'はい' : 'いいえ'}</p>
                    {verificationResult.user && (
                      <>
                        <p><strong>ユーザーID:</strong> {verificationResult.user.uid}</p>
                        <p><strong>メールアドレス:</strong> {verificationResult.user.email}</p>
                        <p><strong>認証プロバイダ:</strong> {verificationResult.user.provider_id || 'email/password'}</p>
                      </>
                    )}
                    <p className="mb-0"><strong>メッセージ:</strong> {verificationResult.message}</p>
                  </Alert>
                </div>
              )}
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </>
  );
};

export default AuthTestPage;
