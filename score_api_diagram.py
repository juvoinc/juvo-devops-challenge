#!/usr/bin/env python3
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import ECS, ECR, ElasticContainerServiceContainer
from diagrams.aws.network import VPC, InternetGateway, NATGateway, ELB, Route53
from diagrams.aws.security import ACM, IAM
from diagrams.aws.management import Cloudwatch
from diagrams.aws.general import InternetAlt1
from diagrams.aws.integration import ApplicationIntegration

# Configuração do diagrama com orientação horizontal e título no topo
graph_attr = {
    "fontsize": "30",
    "bgcolor": "white",
    "pad": "0.75",
    "rankdir": "LR",  # Layout da esquerda para direita (horizontal)
    "splines": "ortho",  # Linhas ortogonais para conexões mais limpas
    "nodesep": "0.6",  # Espaçamento entre nós
    "ranksep": "0.8",   # Espaçamento entre ranks
    "labelloc": "t",   # Posiciona o título no topo (top)
    "labeljust": "c"   # Centraliza o título horizontalmente
}

# Criação do diagrama principal com orientação horizontal
with Diagram("API de Score de Crédito - Arquitetura AWS", show=True, filename="score_api_architecture", 
             graph_attr=graph_attr, direction="LR"):  # Direção explícita LR (left to right)
    
    # Internet e serviços externos (coluna 1)
    internet = InternetAlt1("Internet")
    
    # Serviços de DNS e certificados (coluna 2)
    with Cluster("DNS e Certificados"):
        dns_group = [
            Route53("Route 53"),
            ACM("Certificate Manager")
        ]
    
    # VPC e recursos de rede (coluna 3-5)
    with Cluster("VPC (10.0.0.0/16)"):
        
        # Internet Gateway (entrada da VPC)
        igw = InternetGateway("Internet\nGateway")
        
        # Subnets públicas (coluna 3)
        with Cluster("Subnets Públicas"):
            # Load Balancer
            alb = ELB("Application\nLoad Balancer")
            
            # NAT Gateway
            nat = NATGateway("NAT\nGateway")
        
        # Subnets privadas com ECS Tasks (coluna 4)
        with Cluster("Subnets Privadas"):
            with Cluster("AZ: us-east-1a"):
                task1 = ElasticContainerServiceContainer("ECS Fargate\nTask 1")
            
            with Cluster("AZ: us-east-1b"):
                task2 = ElasticContainerServiceContainer("ECS Fargate\nTask 2")
        
        # Auto Scaling (entre subnets privadas e serviços de gerenciamento)
        auto_scaling = ApplicationIntegration("Auto\nScaling")
    
    # Serviços de gerenciamento e registro (coluna 6)
    with Cluster("Serviços de Gerenciamento"):
        mgmt_services = [
            ECR("Elastic Container\nRegistry"),
            ECS("ECS Cluster"),
            Cloudwatch("CloudWatch"),
            Cloudwatch("CloudWatch\nLogs"),
            IAM("IAM Roles")
        ]
    
    # Conexões - Fluxo de Internet para dentro
    internet >> dns_group[0] >> alb
    internet >> igw >> alb
    dns_group[1] >> alb
    
    # Conexões - ALB para Tasks
    alb >> Edge(color="blue", label="HTTPS") >> task1
    alb >> Edge(color="blue", label="HTTPS") >> task2
    
    # Conexões - Tasks para Internet (via NAT)
    task1 >> Edge(style="dashed", color="darkgreen") >> nat
    task2 >> Edge(style="dashed", color="darkgreen") >> nat
    nat >> igw
    
    # Conexões - Auto Scaling para Tasks
    auto_scaling >> Edge(color="orange") >> task1
    auto_scaling >> Edge(color="orange") >> task2
    
    # Conexões - Serviços de gerenciamento para Tasks
    mgmt_services[0] >> Edge(color="brown") >> task1  # ECR para Task1
    mgmt_services[0] >> Edge(color="brown") >> task2  # ECR para Task2
    
    mgmt_services[1] >> Edge(color="brown") >> task1  # ECS para Task1
    mgmt_services[1] >> Edge(color="brown") >> task2  # ECS para Task2
    
    task1 >> Edge(color="purple") >> mgmt_services[3]  # Task1 para CloudWatch Logs
    task2 >> Edge(color="purple") >> mgmt_services[3]  # Task2 para CloudWatch Logs
    mgmt_services[3] >> mgmt_services[2]  # CloudWatch Logs para CloudWatch
    
    mgmt_services[4] >> Edge(color="red") >> task1  # IAM para Task1
    mgmt_services[4] >> Edge(color="red") >> task2  # IAM para Task2
