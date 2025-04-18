import React from 'react';
import { Card, Row, Col } from 'react-bootstrap';

const AboutPage = () => {
  return (
    <>
      <Row className="mb-4">
        <Col>
          <Card>
            <Card.Body>
              <Card.Title as="h1">このサイトについて</Card.Title>
              <Card.Text>
                このアプリケーションは、ユーザープロフィール管理のためのシンプルなウェブアプリケーションです。
                React、Firebase Authentication、およびバックエンドAPIを使用して構築されています。
              </Card.Text>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      <Row>
        <Col md={6}>
          <Card className="mb-4">
            <Card.Header className="bg-primary text-white">
              <h5 className="mb-0">技術スタック</h5>
            </Card.Header>
            <Card.Body>
              <ul className="list-unstyled">
                <li className="mb-2">
                  <strong>フロントエンド:</strong> React、React Router、React Bootstrap
                </li>
                <li className="mb-2">
                  <strong>認証:</strong> Firebase Authentication
                </li>
                <li className="mb-2">
                  <strong>バックエンド:</strong> Python Flask API
                </li>
                <li className="mb-2">
                  <strong>ビルドツール:</strong> Vite
                </li>
              </ul>
            </Card.Body>
          </Card>
        </Col>

        <Col md={6}>
          <Card className="mb-4">
            <Card.Header className="bg-info text-white">
              <h5 className="mb-0">プロジェクトの目的</h5>
            </Card.Header>
            <Card.Body>
              <p>
                このプロジェクトは、モダンなウェブ開発技術を使用した
                シンプルなユーザー管理システムを構築することを目的としています。
                以下の機能を提供します：
              </p>
              <ul>
                <li>ユーザー登録とログイン</li>
                <li>プロフィール情報の管理</li>
                <li>セキュアなAPI通信</li>
              </ul>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </>
  );
};

export default AboutPage;
