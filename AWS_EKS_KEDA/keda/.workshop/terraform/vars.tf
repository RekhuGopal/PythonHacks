# tflint-ignore: terraform_unused_declarations
variable "eks_cluster_version" {
  description = "EKS cluster version"
  type        = string
}

# tflint-ignore: terraform_unused_declarations
variable "cluster_security_group_id" {
  description = "EKS cluster security group ID"
  type        = any
}


variable "cluster_id" {
  description = "cluster_id"
  type        = any
}

variable "cluster_endpoint" {
  description = "cluster_endpoint"
  type        = any
}

variable "oidc_provider_arn" {
  description = "oidc_provider_arn"
  type        = any
}

# tflint-ignore: terraform_unused_declarations
variable "tags" {
  description = "Tags to apply to AWS resources"
  type        = any
}


variable "load_balancer_controller_chart_version" {
  description = "The chart version of aws-load-balancer-controller to use"
  type        = string
  # renovate-helm: depName=aws-load-balancer-controller
  default = "2.8.1"
}

variable "keda_chart_version" {
  description = "The chart version of keda to use"
  type        = string
  # renovate-helm: depName=keda registryUrl=https://kedacore.github.io/charts
  default = "2.15.0"
}

variable "cluster_name" {
  description = "Name of the EKS cluster"
  type        = string
  default     = "eks-workshop"
}