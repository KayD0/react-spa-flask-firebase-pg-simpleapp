output "db_instance_id" {
  description = "The ID of the RDS instance"
  value       = aws_db_instance.main.id
}

output "db_instance_address" {
  description = "The address of the RDS instance"
  value       = aws_db_instance.main.address
}

output "db_instance_endpoint" {
  description = "The endpoint of the RDS instance"
  value       = aws_db_instance.main.endpoint
}

output "db_instance_port" {
  description = "The port of the RDS instance"
  value       = aws_db_instance.main.port
}

output "db_security_group_id" {
  description = "The ID of the RDS security group"
  value       = aws_security_group.rds.id
}

output "db_subnet_group_id" {
  description = "The ID of the RDS subnet group"
  value       = aws_db_subnet_group.main.id
}

output "db_parameter_group_id" {
  description = "The ID of the RDS parameter group"
  value       = aws_db_parameter_group.main.id
}
