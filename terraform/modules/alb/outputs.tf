output "frontend_alb_id" {
  description = "The ID of the frontend ALB"
  value       = aws_lb.frontend.id
}

output "frontend_alb_dns_name" {
  description = "The DNS name of the frontend ALB"
  value       = aws_lb.frontend.dns_name
}

output "frontend_alb_zone_id" {
  description = "The zone ID of the frontend ALB"
  value       = aws_lb.frontend.zone_id
}

output "frontend_target_group_arn" {
  description = "The ARN of the frontend target group"
  value       = aws_lb_target_group.frontend.arn
}

output "backend_alb_id" {
  description = "The ID of the backend ALB"
  value       = aws_lb.backend.id
}

output "backend_alb_dns_name" {
  description = "The DNS name of the backend ALB"
  value       = aws_lb.backend.dns_name
}

output "backend_alb_zone_id" {
  description = "The zone ID of the backend ALB"
  value       = aws_lb.backend.zone_id
}

output "backend_target_group_arn" {
  description = "The ARN of the backend target group"
  value       = aws_lb_target_group.backend.arn
}

output "alb_security_group_id" {
  description = "The ID of the ALB security group"
  value       = aws_security_group.alb.id
}
