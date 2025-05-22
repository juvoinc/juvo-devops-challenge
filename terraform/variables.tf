variable "aws_region" {
  description = "Região da AWS onde os recursos serão criados"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Nome do projeto, usado como prefixo para recursos"
  type        = string
  default     = "score-api"
}

variable "vpc_cidr" {
  description = "CIDR block para a VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "availability_zones" {
  description = "Lista de zonas de disponibilidade"
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b"]
}

variable "container_port" {
  description = "Porta exposta pelo container"
  type        = number
  default     = 8080
}

variable "domain_name" {
  description = "Nome de domínio para o serviço"
  type        = string
  default     = "api.juvo.turatti.xyz"
}

variable "route53_zone_name" {
  description = "Nome da zona Route53 (domínio raiz)"
  type        = string
  default     = "juvo.turatti.xyz"
}

variable "task_cpu" {
  description = "Unidades de CPU para a tarefa ECS (1024 = 1 vCPU)"
  type        = number
  default     = 1024
}

variable "task_memory" {
  description = "Memória para a tarefa ECS em MB"
  type        = number
  default     = 2048
}

variable "service_desired_count" {
  description = "Número desejado de instâncias da tarefa"
  type        = number
  default     = 2
}

variable "auto_scaling_min_capacity" {
  description = "Capacidade mínima para auto scaling"
  type        = number
  default     = 2
}

variable "auto_scaling_max_capacity" {
  description = "Capacidade máxima para auto scaling"
  type        = number
  default     = 10
}

variable "ecr_repository_url" {
  description = "URL do repositório ECR (será preenchido pelo output)"
  type        = string
}