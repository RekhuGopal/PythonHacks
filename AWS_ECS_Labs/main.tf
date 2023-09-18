/*
module "ecs" {
  source                  = "./ECS"
  vpc_id                  = "vpc-29568551"
  cluster_name            = "demo-api-cluster"
  cluster_service_name    = "cloudquicklabs-api-service"
  cluster_service_task_name = "cloudquicklabs-api-task"
  vpc_id_subnet_list      = ["subnet-470f460c", "	subnet-34b48b6e", "subnet-9b072be2", "subnet-f78ebadf"]
  execution_role_arn      = "arn:aws:iam::357171621133:role/ETLlambdaAccessRole"
  image_id                = "357171621133.dkr.ecr.us-west-2.amazonaws.com/ecsdemo:latest"
}
*/
