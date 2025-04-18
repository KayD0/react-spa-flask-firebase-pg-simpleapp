import React, { useState } from 'react';
import { Card, Form, Button, Alert, Row, Col } from 'react-bootstrap';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const RegisterPage = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: ''
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');
  const { signUp } = useAuth();
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

    // Validate passwords match
    if (formData.password !== formData.confirmPassword) {
      setError('パスワードが一致しません');
      return;
    }

    // Validate password strength
    if (formData.password.length < 6) {
      setError('パスワードは6文字以上である必要があります');
      return;
    }

    setIsSubmitting(true);

    try {
      const { email, password } = formData;
      const { user, error: signUpError } = await signUp(email, password);

      if (signUpError) {
        setError(signUpError);
      } else {
        // Redirect to home page on successful registration
        navigate('/');
      }
    } catch (err) {
      console.error('Registration error:', err);
      setError('登録処理中にエラーが発生しました。後でもう一度お試しください。');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Row className="justify-content-center">
      <Col md={6}>
        <Card>
          <Card.Header>
            <h2 className="card-title mb-0">アカウント登録</h2>
          </Card.Header>
          <Card.Body>
            {error && (
              <Alert variant="danger" dismissible onClose={() => setError('')}>
                {error}
              </Alert>
            )}

            <Form onSubmit={handleSubmit}>
              <Form.Group className="mb-3" controlId="registerEmail">
                <Form.Label>メールアドレス</Form.Label>
                <Form.Control
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  required
                />
              </Form.Group>

              <Form.Group className="mb-3" controlId="registerPassword">
                <Form.Label>パスワード</Form.Label>
                <Form.Control
                  type="password"
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  required
                />
                <Form.Text className="text-muted">
                  パスワードは6文字以上である必要があります。
                </Form.Text>
              </Form.Group>

              <Form.Group className="mb-3" controlId="registerConfirmPassword">
                <Form.Label>パスワード（確認）</Form.Label>
                <Form.Control
                  type="password"
                  name="confirmPassword"
                  value={formData.confirmPassword}
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
                  ) : '登録'}
                </Button>
                <Link to="/login">すでにアカウントをお持ちの方はログイン</Link>
              </div>
            </Form>
          </Card.Body>
        </Card>
      </Col>
    </Row>
  );
};

export default RegisterPage;
