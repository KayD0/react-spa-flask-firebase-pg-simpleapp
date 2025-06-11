# Security group for the ALB
resource "aws_security_group" "alb" {
  name        = "${var.environment}-alb-sg"
  description = "Security group for the ALB"
  vpc_id      = var.vpc_id

  # Allow HTTP traffic from anywhere
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow HTTPS traffic from anywhere
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow all outbound traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "${var.environment}-alb-sg"
    Environment = var.environment
  }
}

# Frontend ALB
resource "aws_lb" "frontend" {
  name               = "${var.environment}-frontend-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = var.public_subnets

  enable_deletion_protection = false

  tags = {
    Name        = "${var.environment}-frontend-alb"
    Environment = var.environment
  }
}

# Frontend ALB target group
resource "aws_lb_target_group" "frontend" {
  name     = "${var.environment}-frontend-tg"
  port     = var.frontend_port
  protocol = var.frontend_protocol
  vpc_id   = var.vpc_id
  
  target_type = "ip"

  health_check {
    enabled             = true
    interval            = 30
    path                = "/"
    port                = "traffic-port"
    healthy_threshold   = 3
    unhealthy_threshold = 3
    timeout             = 5
    protocol            = var.frontend_protocol
    matcher             = "200-299"
  }

  tags = {
    Name        = "${var.environment}-frontend-tg"
    Environment = var.environment
  }
}

# Frontend ALB listener
resource "aws_lb_listener" "frontend_http" {
  load_balancer_arn = aws_lb.frontend.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.frontend.arn
  }
}

# Backend ALB
resource "aws_lb" "backend" {
  name               = "${var.environment}-backend-alb"
  internal           = true
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = var.public_subnets

  enable_deletion_protection = false

  tags = {
    Name        = "${var.environment}-backend-alb"
    Environment = var.environment
  }
}

# Backend ALB target group
resource "aws_lb_target_group" "backend" {
  name     = "${var.environment}-backend-tg"
  port     = var.backend_port
  protocol = var.backend_protocol
  vpc_id   = var.vpc_id
  
  target_type = "ip"

  health_check {
    enabled             = true
    interval            = 30
    path                = "/api/health"
    port                = "traffic-port"
    healthy_threshold   = 3
    unhealthy_threshold = 3
    timeout             = 5
    protocol            = var.backend_protocol
    matcher             = "200-299"
  }

  tags = {
    Name        = "${var.environment}-backend-tg"
    Environment = var.environment
  }
}

# Backend ALB listener
resource "aws_lb_listener" "backend_http" {
  load_balancer_arn = aws_lb.backend.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.backend.arn
  }
}
