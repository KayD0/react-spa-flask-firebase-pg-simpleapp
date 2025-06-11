provider "aws" {
  region = var.aws_region
}

module "vpc" {
  source = "./modules/vpc"

  environment     = var.environment
  vpc_cidr        = var.vpc_cidr
  azs             = var.availability_zones
  private_subnets = var.private_subnets
  public_subnets  = var.public_subnets
}

module "alb" {
  source = "./modules/alb"

  environment    = var.environment
  vpc_id         = module.vpc.vpc_id
  public_subnets = module.vpc.public_subnet_ids
}

module "ecs" {
  source = "./modules/ecs"

  environment        = var.environment
  vpc_id             = module.vpc.vpc_id
  private_subnet_ids = module.vpc.private_subnet_ids
  
  frontend_alb_target_group_arn = module.alb.frontend_target_group_arn
  backend_alb_target_group_arn  = module.alb.backend_target_group_arn
  
  frontend_image = var.frontend_image
  backend_image  = var.backend_image
  
  db_host     = module.rds.db_instance_address
  db_port     = module.rds.db_instance_port
  db_name     = var.db_name
  db_username = var.db_username
  db_password = var.db_password
  
  aws_region           = var.aws_region
  alb_security_group_id = module.alb.alb_security_group_id
  backend_alb_dns_name = module.alb.backend_alb_dns_name
}

module "rds" {
  source = "./modules/rds"

  environment        = var.environment
  vpc_id             = module.vpc.vpc_id
  private_subnet_ids = module.vpc.private_subnet_ids
  
  db_name     = var.db_name
  db_username = var.db_username
  db_password = var.db_password
  
  db_instance_class = var.db_instance_class
  db_engine_version = var.db_engine_version
}
