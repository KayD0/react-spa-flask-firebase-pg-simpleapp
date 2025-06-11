# VPC Outputs
output "vpc_id" {
  description = "The ID of the VPC"
  value       = module.vpc.vpc_id
}

output "public_subnet_ids" {
  description = "List of public subnet IDs"
  value       = module.vpc.public_subnet_ids
}

output "private_subnet_ids" {
  description = "List of private subnet IDs"
  value       = module.vpc.private_subnet_ids
}

# ALB Outputs
output "frontend_alb_dns_name" {
  description = "The DNS name of the frontend ALB"
  value       = module.alb.frontend_alb_dns_name
}

output "frontend_alb_zone_id" {
  description = "The zone ID of the frontend ALB"
  value       = module.alb.frontend_alb_zone_id
}

output "backend_alb_dns_name" {
  description = "The DNS name of the backend ALB"
  value       = module.alb.backend_alb_dns_name
}

# ECS Outputs
output "ecs_cluster_name" {
  description = "The name of the ECS cluster"
  value       = module.ecs.ecs_cluster_name
}

output "frontend_service_id" {
  description = "The ID of the frontend ECS service"
  value       = module.ecs.frontend_service_id
}

output "backend_service_id" {
  description = "The ID of the backend ECS service"
  value       = module.ecs.backend_service_id
}

# RDS Outputs
output "db_instance_endpoint" {
  description = "The endpoint of the RDS instance"
  value       = module.rds.db_instance_endpoint
}

output "db_instance_address" {
  description = "The address of the RDS instance"
  value       = module.rds.db_instance_address
}

# Application URLs
output "frontend_url" {
  description = "URL to access the frontend application"
  value       = "http://${module.alb.frontend_alb_dns_name}"
}

output "backend_api_url" {
  description = "URL to access the backend API"
  value       = "http://${module.alb.backend_alb_dns_name}"
}
