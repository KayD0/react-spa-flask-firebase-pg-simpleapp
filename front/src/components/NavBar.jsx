import React from 'react';
import { Navbar, Container, Nav, Button } from 'react-bootstrap';
import { Link, NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const NavBar = () => {
  const { isAuthenticated, signOut, currentUser } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      const { error } = await signOut();
      if (!error) {
        navigate('/');
      } else {
        console.error('Logout error:', error);
      }
    } catch (err) {
      console.error('Logout error:', err);
    }
  };

  return (
    <Navbar bg="dark" variant="dark" expand="lg" className="mb-4">
      <Container fluid>
        <Navbar.Brand as={Link} to="/">ユーザープロフィールアプリ</Navbar.Brand>
        <Navbar.Toggle aria-controls="navbarNav" />
        <Navbar.Collapse id="navbarNav">
          <Nav className="me-auto">
            <Nav.Link as={NavLink} to="/">ホーム</Nav.Link>
            <Nav.Link as={NavLink} to="/about">このサイトについて</Nav.Link>
            <Nav.Link as={NavLink} to="/contact">お問い合わせ</Nav.Link>
          </Nav>
          <Nav>
            {isAuthenticated ? (
              <>
                <Nav.Link as={NavLink} to="/profile">プロフィール</Nav.Link>
                <Nav.Link as={NavLink} to="/auth-test">認証テスト</Nav.Link>
                <Button 
                  variant="link" 
                  className="nav-link" 
                  onClick={handleLogout}
                >
                  ログアウト
                </Button>
              </>
            ) : (
              <>
                <Nav.Link as={NavLink} to="/login">ログイン</Nav.Link>
                <Nav.Link as={NavLink} to="/register">登録</Nav.Link>
              </>
            )}
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default NavBar;
