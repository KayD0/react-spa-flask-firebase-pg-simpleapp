output "ecs_cluster_id" {
  description = "The ID of the ECS cluster"
  value       = aws_ecs_cluster.main.id
}

output "ecs_cluster_name" {
  description = "The name of the ECS cluster"
  value       = aws_ecs_cluster.main.name
}

output "ecs_task_execution_role_arn" {
  description = "The ARN of the ECS task execution role"
  value       = aws_iam_role.ecs_task_execution_role.arn
}

output "ecs_task_role_arn" {
  description = "The ARN of the ECS task role"
  value       = aws_iam_role.ecs_task_role.arn
}

output "frontend_task_definition_arn" {
  description = "The ARN of the frontend task definition"
  value       = aws_ecs_task_definition.frontend.arn
}

output "backend_task_definition_arn" {
  description = "The ARN of the backend task definition"
  value       = aws_ecs_task_definition.backend.arn
}

output "frontend_service_id" {
  description = "The ID of the frontend ECS service"
  value       = aws_ecs_service.frontend.id
}

output "backend_service_id" {
  description = "The ID of the backend ECS service"
  value       = aws_ecs_service.backend.id
}

output "ecs_security_group_id" {
  description = "The ID of the ECS security group"
  value       = aws_security_group.ecs_tasks.id
}
