import React from 'react';
import { Row, Col, Card, Badge, ListGroup } from 'react-bootstrap';

const HomePage = () => {
  return (
    <>
      <Row className="mb-4">
        <Col xs={12}>
          <Card>
            <Card.Body>
              <Card.Title as="h1">ユーザープロフィールアプリ</Card.Title>
              <Card.Text>シンプルなユーザープロフィール管理アプリケーション</Card.Text>
            </Card.Body>
          </Card>
        </Col>
      </Row>
      
      <Row>
        <Col md={6}>
          <Card className="mb-4">
            <Card.Header className="bg-primary text-white">
              <h5 className="mb-0">機能一覧</h5>
            </Card.Header>
            <Card.Body>
              <ListGroup variant="flush">
                <ListGroup.Item className="d-flex justify-content-between align-items-center">
                  ユーザー登録
                  <Badge bg="success" pill>利用可能</Badge>
                </ListGroup.Item>
                <ListGroup.Item className="d-flex justify-content-between align-items-center">
                  ログイン/ログアウト
                  <Badge bg="success" pill>利用可能</Badge>
                </ListGroup.Item>
                <ListGroup.Item className="d-flex justify-content-between align-items-center">
                  プロフィール編集
                  <Badge bg="success" pill>利用可能</Badge>
                </ListGroup.Item>
              </ListGroup>
            </Card.Body>
          </Card>
        </Col>
        
        <Col md={6}>
          <Card className="mb-4">
            <Card.Header className="bg-info text-white">
              <h5 className="mb-0">使い方</h5>
            </Card.Header>
            <Card.Body>
              <ListGroup variant="flush" numbered>
                <ListGroup.Item>右上の「登録」からアカウントを作成</ListGroup.Item>
                <ListGroup.Item>作成したアカウントでログイン</ListGroup.Item>
                <ListGroup.Item>プロフィールページで個人情報を編集</ListGroup.Item>
              </ListGroup>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </>
  );
};

export default HomePage;
