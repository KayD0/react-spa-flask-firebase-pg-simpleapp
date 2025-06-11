aws_region = "ap-northeast-1"  # Tokyo region
environment = "dev"

# VPC Configuration
vpc_cidr           = "10.0.0.0/16"
availability_zones = ["ap-northeast-1a", "ap-northeast-1c"]
private_subnets    = ["10.0.1.0/24", "10.0.2.0/24"]
public_subnets     = ["10.0.101.0/24", "10.0.102.0/24"]

# Container Images
frontend_image = "your-account-id.dkr.ecr.ap-northeast-1.amazonaws.com/frontend:latest"
backend_image  = "your-account-id.dkr.ecr.ap-northeast-1.amazonaws.com/backend:latest"

# Database Configuration
db_name           = "appdb"
db_username       = "dbuser"
db_password       = "dbpassword"  # In production, use AWS Secrets Manager or similar
db_instance_class = "db.t3.micro"
db_engine_version = "13.7"
