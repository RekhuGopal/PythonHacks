

data "aws_vpc" "existing" {
  id = var.vpc_id  
}


resource "aws_security_group" "ecs_sg" {
  vpc_id = data.aws_vpc.existing.id
  name   = "ecs-security-group"
  # Inbound and outbound rules
  ingress {
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}


resource "aws_ecs_task_definition" "task_definition" {
  family                = var.cluster_service_task_name
  network_mode          = "awsvpc"
  memory                = "512"
  requires_compatibilities = ["FARGATE"]


  execution_role_arn    = var.execution_role_arn 


  container_definitions = jsonencode([
    {
      name      = "flask-api-container"
      image     = var.image_id  
      cpu       = 256
      memory    = 512
      port_mappings = [
        {
          container_port = 5000
          host_port      = 5000
          protocol       = "tcp"
        }
      ]
    }
  ])

  cpu = "256"  
}


resource "aws_ecs_cluster" "ecs_cluster" {
  name = var.cluster_name
}

resource "aws_ecs_service" "service" {
  name            = var.cluster_service_name
  cluster         = aws_ecs_cluster.ecs_cluster.id
  task_definition = aws_ecs_task_definition.task_definition.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = [var.vpc_id_subnet_list[0], var.vpc_id_subnet_list[1], var.vpc_id_subnet_list[2], var.vpc_id_subnet_list[3]]
    security_groups  = [aws_security_group.ecs_sg.id]
    assign_public_ip = true
  }
}