variable "aws_region" {
  description = "The AWS region to deploy resources"
  type        = string
  default     = "ap-northeast-1"  # Tokyo region
}

variable "environment" {
  description = "Environment name (e.g., dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "availability_zones" {
  description = "List of availability zones to use"
  type        = list(string)
  default     = ["ap-northeast-1a", "ap-northeast-1c"]
}

variable "private_subnets" {
  description = "List of private subnet CIDR blocks"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "public_subnets" {
  description = "List of public subnet CIDR blocks"
  type        = list(string)
  default     = ["10.0.101.0/24", "10.0.102.0/24"]
}

variable "frontend_image" {
  description = "Docker image for the frontend application"
  type        = string
  default     = "frontend:latest"
}

variable "backend_image" {
  description = "Docker image for the backend application"
  type        = string
  default     = "backend:latest"
}

variable "db_name" {
  description = "Name of the PostgreSQL database"
  type        = string
  default     = "appdb"
}

variable "db_username" {
  description = "Username for the PostgreSQL database"
  type        = string
  default     = "dbuser"
  sensitive   = true
}

variable "db_password" {
  description = "Password for the PostgreSQL database"
  type        = string
  default     = "dbpassword"  # In production, use AWS Secrets Manager or similar
  sensitive   = true
}

variable "db_instance_class" {
  description = "Instance class for the RDS instance"
  type        = string
  default     = "db.t3.micro"
}

variable "db_engine_version" {
  description = "PostgreSQL engine version"
  type        = string
  default     = "13.7"
}
