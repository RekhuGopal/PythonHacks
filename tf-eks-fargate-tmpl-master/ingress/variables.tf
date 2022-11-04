variable "name" {
  description = "the name of your stack, e.g. \"demo\""
}

variable "environment" {
  description = "the name of your environment, e.g. \"prod\""
}

variable "region" {
  description = "the AWS region in which resources are created, you must set the availability_zones variable as well if you define this value to something other than the default"
}

variable "vpc_id" {
  description = "The VPC the cluser should be created in"
}

variable "cluster_id" {
  description = "The ID of the cluster where the ingress controller should be attached"
}