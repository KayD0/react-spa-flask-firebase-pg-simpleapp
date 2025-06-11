variable "environment" {
  description = "Environment name (e.g., dev, staging, prod)"
  type        = string
}

variable "vpc_id" {
  description = "The ID of the VPC"
  type        = string
}

variable "private_subnet_ids" {
  description = "List of private subnet IDs"
  type        = list(string)
}

variable "frontend_alb_target_group_arn" {
  description = "ARN of the frontend ALB target group"
  type        = string
}

variable "backend_alb_target_group_arn" {
  description = "ARN of the backend ALB target group"
  type        = string
}

variable "frontend_container_port" {
  description = "Port for the frontend container"
  type        = number
  default     = 80
}

variable "backend_container_port" {
  description = "Port for the backend container"
  type        = number
  default     = 8080
}

variable "frontend_image" {
  description = "Docker image for the frontend application"
  type        = string
}

variable "backend_image" {
  description = "Docker image for the backend application"
  type        = string
}

variable "db_host" {
  description = "Host of the PostgreSQL database"
  type        = string
}

variable "db_port" {
  description = "Port of the PostgreSQL database"
  type        = number
  default     = 5432
}

variable "db_name" {
  description = "Name of the PostgreSQL database"
  type        = string
}

variable "db_username" {
  description = "Username for the PostgreSQL database"
  type        = string
}

variable "db_password" {
  description = "Password for the PostgreSQL database"
  type        = string
  sensitive   = true
}

variable "aws_region" {
  description = "The AWS region to deploy resources"
  type        = string
}

variable "alb_security_group_id" {
  description = "The ID of the ALB security group"
  type        = string
}

variable "backend_alb_dns_name" {
  description = "The DNS name of the backend ALB"
  type        = string
}
