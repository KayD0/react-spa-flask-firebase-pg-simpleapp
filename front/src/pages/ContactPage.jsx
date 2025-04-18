import React, { useState } from 'react';
import { Card, Form, Button, Alert, Row, Col } from 'react-bootstrap';

const ContactPage = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    message: ''
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitResult, setSubmitResult] = useState({
    success: false,
    message: '',
    show: false
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setSubmitResult({ success: false, message: '', show: false });

    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Simulate successful submission
      setSubmitResult({
        success: true,
        message: 'お問い合わせが送信されました。ありがとうございます。',
        show: true
      });
      
      // Reset form
      setFormData({
        name: '',
        email: '',
        message: ''
      });
    } catch (error) {
      console.error('Contact form submission error:', error);
      setSubmitResult({
        success: false,
        message: 'エラーが発生しました。後でもう一度お試しください。',
        show: true
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <>
      <Row className="mb-4">
        <Col>
          <Card>
            <Card.Body>
              <Card.Title as="h1">お問い合わせ</Card.Title>
              <Card.Text>
                ご質問やフィードバックがありましたら、以下のフォームからお気軽にお問い合わせください。
              </Card.Text>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      <Row>
        <Col md={8}>
          <Card>
            <Card.Body>
              {submitResult.show && (
                <Alert 
                  variant={submitResult.success ? 'success' : 'danger'}
                  dismissible
                  onClose={() => setSubmitResult(prev => ({ ...prev, show: false }))}
                >
                  {submitResult.message}
                </Alert>
              )}

              <Form onSubmit={handleSubmit}>
                <Form.Group className="mb-3" controlId="contactName">
                  <Form.Label>お名前</Form.Label>
                  <Form.Control
                    type="text"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    required
                  />
                </Form.Group>

                <Form.Group className="mb-3" controlId="contactEmail">
                  <Form.Label>メールアドレス</Form.Label>
                  <Form.Control
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    required
                  />
                </Form.Group>

                <Form.Group className="mb-3" controlId="contactMessage">
                  <Form.Label>メッセージ</Form.Label>
                  <Form.Control
                    as="textarea"
                    rows={5}
                    name="message"
                    value={formData.message}
                    onChange={handleChange}
                    required
                  />
                </Form.Group>

                <Button 
                  variant="primary" 
                  type="submit" 
                  disabled={isSubmitting}
                >
                  {isSubmitting ? (
                    <>
                      <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                      送信中...
                    </>
                  ) : '送信'}
                </Button>
              </Form>
            </Card.Body>
          </Card>
        </Col>

        <Col md={4}>
          <Card className="mb-4">
            <Card.Header className="bg-info text-white">
              <h5 className="mb-0">連絡先情報</h5>
            </Card.Header>
            <Card.Body>
              <p><strong>メール:</strong> support@example.com</p>
              <p><strong>電話:</strong> 03-1234-5678</p>
              <p><strong>営業時間:</strong> 平日 9:00 - 18:00</p>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </>
  );
};

export default ContactPage;
