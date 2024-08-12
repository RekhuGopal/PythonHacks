data "aws_partition" "current" {}
data "aws_eks_cluster" "cluster" {
  name = "eks-workshop"
}

data "aws_eks_cluster_auth" "cluster" {
  name = "eks-workshop"
}
module "eks_blueprints_addons" {
  source  = "aws-ia/eks-blueprints-addons/aws"
  version = "1.16.3"

  cluster_name      = var.cluster_name
  cluster_endpoint  = var.cluster_endpoint
  cluster_version   = var.eks_cluster_version
  oidc_provider_arn = var.oidc_provider_arn

  enable_aws_load_balancer_controller = true
}

module "iam_assumable_role_keda" {
  source                        = "terraform-aws-modules/iam/aws//modules/iam-assumable-role-with-oidc"
  version                       = "5.39.1"
  create_role                   = true
  role_name                     = "iam-keda-role"
  provider_url                  = var.oidc_provider_arn
  role_policy_arns              = ["arn:${data.aws_partition.current.partition}:iam::aws:policy/CloudWatchReadOnlyAccess"]
  oidc_fully_qualified_subjects = ["system:serviceaccount:keda:keda-operator"]

  tags = var.tags
}

/*
provider "kubernetes" {
  host                   = data.aws_eks_cluster.cluster.endpoint
  token                  = data.aws_eks_cluster_auth.cluster.token
  cluster_ca_certificate = base64decode(data.aws_eks_cluster.cluster.certificate_authority[0].data)
}


resource "kubernetes_manifest" "ui_alb" {
  manifest = {
    "apiVersion" = "networking.k8s.io/v1"
    "kind"       = "Ingress"
    "metadata" = {
      "name"      = "ui"
      "namespace" = "ui"
      "annotations" = {
        "alb.ingress.kubernetes.io/scheme"           = "internet-facing"
        "alb.ingress.kubernetes.io/target-type"      = "ip"
        "alb.ingress.kubernetes.io/healthcheck-path" = "/actuator/health/liveness"
      }
    }
    "spec" = {
      ingressClassName = "alb",
      "rules" = [{
        "http" = {
          paths = [{
            path     = "/"
            pathType = "Prefix"
            "backend" = {
              service = {
                name = "ui"
                port = {
                  number = 80
                }
              }
            }
          }]
        }
      }]
    }
  }
}
*/
