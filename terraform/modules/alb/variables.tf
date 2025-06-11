variable "environment" {
  description = "Environment name (e.g., dev, staging, prod)"
  type        = string
}

variable "vpc_id" {
  description = "The ID of the VPC"
  type        = string
}

variable "public_subnets" {
  description = "List of public subnet IDs"
  type        = list(string)
}

variable "frontend_port" {
  description = "Port for the frontend target group"
  type        = number
  default     = 80
}

variable "frontend_protocol" {
  description = "Protocol for the frontend target group"
  type        = string
  default     = "HTTP"
}

variable "backend_port" {
  description = "Port for the backend target group"
  type        = number
  default     = 8080
}

variable "backend_protocol" {
  description = "Protocol for the backend target group"
  type        = string
  default     = "HTTP"
}
