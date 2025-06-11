# ECS Cluster
resource "aws_ecs_cluster" "main" {
  name = "${var.environment}-cluster"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }

  tags = {
    Name        = "${var.environment}-cluster"
    Environment = var.environment
  }
}

# Security group for the ECS tasks
resource "aws_security_group" "ecs_tasks" {
  name        = "${var.environment}-ecs-tasks-sg"
  description = "Security group for the ECS tasks"
  vpc_id      = var.vpc_id

  # Allow all outbound traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "${var.environment}-ecs-tasks-sg"
    Environment = var.environment
  }
}

# Allow inbound traffic from ALB to frontend container
resource "aws_security_group_rule" "frontend_inbound" {
  security_group_id        = aws_security_group.ecs_tasks.id
  type                     = "ingress"
  from_port                = var.frontend_container_port
  to_port                  = var.frontend_container_port
  protocol                 = "tcp"
  source_security_group_id = var.alb_security_group_id
  description              = "Allow inbound traffic from ALB to frontend container"
}

# Allow inbound traffic from ALB to backend container
resource "aws_security_group_rule" "backend_inbound" {
  security_group_id        = aws_security_group.ecs_tasks.id
  type                     = "ingress"
  from_port                = var.backend_container_port
  to_port                  = var.backend_container_port
  protocol                 = "tcp"
  source_security_group_id = var.alb_security_group_id
  description              = "Allow inbound traffic from ALB to backend container"
}

# ECS Task Execution Role
resource "aws_iam_role" "ecs_task_execution_role" {
  name = "${var.environment}-ecs-task-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    Name        = "${var.environment}-ecs-task-execution-role"
    Environment = var.environment
  }
}

# Attach the ECS Task Execution Role policy
resource "aws_iam_role_policy_attachment" "ecs_task_execution_role_policy" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# ECS Task Role
resource "aws_iam_role" "ecs_task_role" {
  name = "${var.environment}-ecs-task-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    Name        = "${var.environment}-ecs-task-role"
    Environment = var.environment
  }
}

# Frontend Task Definition
resource "aws_ecs_task_definition" "frontend" {
  family                   = "${var.environment}-frontend"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = 256
  memory                   = 512
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_task_role.arn

  container_definitions = jsonencode([
    {
      name      = "frontend"
      image     = var.frontend_image
      essential = true
      
      portMappings = [
        {
          containerPort = var.frontend_container_port
          hostPort      = var.frontend_container_port
          protocol      = "tcp"
        }
      ]
      
      environment = [
        {
          name  = "REACT_APP_API_URL"
          value = "http://${var.backend_alb_dns_name}"
        }
      ]
      
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = "/ecs/${var.environment}/frontend"
          "awslogs-region"        = var.aws_region
          "awslogs-stream-prefix" = "ecs"
        }
      }
    }
  ])

  tags = {
    Name        = "${var.environment}-frontend-task-definition"
    Environment = var.environment
  }
}

# Backend Task Definition
resource "aws_ecs_task_definition" "backend" {
  family                   = "${var.environment}-backend"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = 256
  memory                   = 512
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_task_role.arn

  container_definitions = jsonencode([
    {
      name      = "backend"
      image     = var.backend_image
      essential = true
      
      portMappings = [
        {
          containerPort = var.backend_container_port
          hostPort      = var.backend_container_port
          protocol      = "tcp"
        }
      ]
      
      environment = [
        {
          name  = "DB_HOST"
          value = var.db_host
        },
        {
          name  = "DB_PORT"
          value = tostring(var.db_port)
        },
        {
          name  = "DB_NAME"
          value = var.db_name
        },
        {
          name  = "DB_USER"
          value = var.db_username
        },
        {
          name  = "DB_PASSWORD"
          value = var.db_password
        }
      ]
      
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = "/ecs/${var.environment}/backend"
          "awslogs-region"        = var.aws_region
          "awslogs-stream-prefix" = "ecs"
        }
      }
    }
  ])

  tags = {
    Name        = "${var.environment}-backend-task-definition"
    Environment = var.environment
  }
}

# CloudWatch Log Groups
resource "aws_cloudwatch_log_group" "frontend" {
  name              = "/ecs/${var.environment}/frontend"
  retention_in_days = 30

  tags = {
    Name        = "${var.environment}-frontend-log-group"
    Environment = var.environment
  }
}

resource "aws_cloudwatch_log_group" "backend" {
  name              = "/ecs/${var.environment}/backend"
  retention_in_days = 30

  tags = {
    Name        = "${var.environment}-backend-log-group"
    Environment = var.environment
  }
}

# Frontend ECS Service
resource "aws_ecs_service" "frontend" {
  name            = "${var.environment}-frontend-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.frontend.arn
  desired_count   = 2
  launch_type     = "FARGATE"

  network_configuration {
    security_groups  = [aws_security_group.ecs_tasks.id]
    subnets          = var.private_subnet_ids
    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = var.frontend_alb_target_group_arn
    container_name   = "frontend"
    container_port   = var.frontend_container_port
  }

  deployment_controller {
    type = "ECS"
  }

  tags = {
    Name        = "${var.environment}-frontend-service"
    Environment = var.environment
  }

  depends_on = [aws_cloudwatch_log_group.frontend]
}

# Backend ECS Service
resource "aws_ecs_service" "backend" {
  name            = "${var.environment}-backend-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.backend.arn
  desired_count   = 2
  launch_type     = "FARGATE"

  network_configuration {
    security_groups  = [aws_security_group.ecs_tasks.id]
    subnets          = var.private_subnet_ids
    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = var.backend_alb_target_group_arn
    container_name   = "backend"
    container_port   = var.backend_container_port
  }

  deployment_controller {
    type = "ECS"
  }

  tags = {
    Name        = "${var.environment}-backend-service"
    Environment = var.environment
  }

  depends_on = [aws_cloudwatch_log_group.backend]
}
