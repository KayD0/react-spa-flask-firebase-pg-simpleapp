# Security group for the RDS instance
resource "aws_security_group" "rds" {
  name        = "${var.environment}-rds-sg"
  description = "Security group for the RDS instance"
  vpc_id      = var.vpc_id

  # Allow PostgreSQL traffic from the private subnets
  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    cidr_blocks     = ["10.0.0.0/8"]  # Assuming VPC CIDR is within this range
    description     = "Allow PostgreSQL traffic from the VPC"
  }

  # Allow all outbound traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "${var.environment}-rds-sg"
    Environment = var.environment
  }
}

# RDS subnet group
resource "aws_db_subnet_group" "main" {
  name       = "${var.environment}-db-subnet-group"
  subnet_ids = var.private_subnet_ids

  tags = {
    Name        = "${var.environment}-db-subnet-group"
    Environment = var.environment
  }
}

# RDS parameter group
resource "aws_db_parameter_group" "main" {
  name   = "${var.environment}-db-parameter-group"
  family = "postgres13"

  parameter {
    name  = "log_connections"
    value = "1"
  }

  parameter {
    name  = "log_disconnections"
    value = "1"
  }

  tags = {
    Name        = "${var.environment}-db-parameter-group"
    Environment = var.environment
  }
}

# RDS instance
resource "aws_db_instance" "main" {
  identifier             = "${var.environment}-db"
  engine                 = "postgres"
  engine_version         = var.db_engine_version
  instance_class         = var.db_instance_class
  allocated_storage      = 20
  max_allocated_storage  = 100
  storage_type           = "gp2"
  storage_encrypted      = true
  
  db_name                = var.db_name
  username               = var.db_username
  password               = var.db_password
  port                   = 5432
  
  vpc_security_group_ids = [aws_security_group.rds.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name
  parameter_group_name   = aws_db_parameter_group.main.name
  
  publicly_accessible    = false
  skip_final_snapshot    = true
  deletion_protection    = false
  
  backup_retention_period = 7
  backup_window           = "03:00-04:00"
  maintenance_window      = "Mon:04:00-Mon:05:00"
  
  tags = {
    Name        = "${var.environment}-db"
    Environment = var.environment
  }
}
