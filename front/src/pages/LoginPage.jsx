import React, { useState } from 'react';
import { Card, Form, Button, Alert, Row, Col } from 'react-bootstrap';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const LoginPage = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');
  const { signIn } = useAuth();
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setIsSubmitting(true);

    try {
      const { email, password } = formData;
      const { user, error: signInError } = await signIn(email, password);

      if (signInError) {
        setError(signInError);
      } else {
        // Redirect to home page on successful login
        navigate('/');
      }
    } catch (err) {
      console.error('Login error:', err);
      setError('ログイン処理中にエラーが発生しました。後でもう一度お試しください。');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Row className="justify-content-center">
      <Col md={6}>
        <Card>
          <Card.Header>
            <h2 className="card-title mb-0">ログイン</h2>
          </Card.Header>
          <Card.Body>
            {error && (
              <Alert variant="danger" dismissible onClose={() => setError('')}>
                {error}
              </Alert>
            )}

            <Form onSubmit={handleSubmit}>
              <Form.Group className="mb-3" controlId="loginEmail">
                <Form.Label>メールアドレス</Form.Label>
                <Form.Control
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  required
                />
              </Form.Group>

              <Form.Group className="mb-3" controlId="loginPassword">
                <Form.Label>パスワード</Form.Label>
                <Form.Control
                  type="password"
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  required
                />
              </Form.Group>

              <div className="d-flex justify-content-between align-items-center">
                <Button 
                  variant="primary" 
                  type="submit" 
                  disabled={isSubmitting}
                >
                  {isSubmitting ? (
                    <>
                      <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                      処理中...
                    </>
                  ) : 'ログイン'}
                </Button>
                <Link to="/register">アカウントをお持ちでない方は登録</Link>
              </div>
            </Form>
          </Card.Body>
        </Card>
      </Col>
    </Row>
  );
};

export default LoginPage;
