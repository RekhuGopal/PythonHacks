
data "aws_iam_policy_document" "lab-backup-service-assume-role-policy-doc" {
  statement {
    sid     = "AssumeServiceRole"
    actions = ["sts:AssumeRole"]
    effect  = "Allow"

    principals {
      type        = "Service"
      identifiers = ["backup.amazonaws.com"]
    }
  }
}


data "aws_iam_policy" "aws-backup-service-policy" {
  arn = "arn:aws:iam::aws:policy/service-role/AWSBackupServiceRolePolicyForBackup"
}

data "aws_iam_policy" "aws-restore-service-policy" {
  arn = "arn:aws:iam::aws:policy/service-role/AWSBackupServiceRolePolicyForRestores"
}

data "aws_caller_identity" "current_account" {}

data "aws_iam_policy_document" "lab-pass-role-policy-doc" {
  statement {
    sid       = "ExamplePassRole"
    actions   = ["iam:PassRole"]
    effect    = "Allow"
    resources = ["arn:aws:iam::${data.aws_caller_identity.current_account.account_id}:role/*"]
  }
}

resource "aws_iam_role" "lab-backup-service-role" {
  name               = "ExampleAWSBackupServiceRole"
  description        = "Allows the AWS Backup Service to take scheduled backups"
  assume_role_policy = data.aws_iam_policy_document.lab-backup-service-assume-role-policy-doc.json

  tags = {
    Project = "CloudQuickLabsDemo"
    Role    = "iam"
  }
}

resource "aws_iam_role_policy" "lab-backup-service-aws-backup-role-policy" {
  policy = data.aws_iam_policy.aws-backup-service-policy.policy
  role   = aws_iam_role.lab-backup-service-role.name
}

resource "aws_iam_role_policy" "lab-restore-service-aws-backup-role-policy" {
  policy = data.aws_iam_policy.aws-restore-service-policy.policy
  role   = aws_iam_role.lab-backup-service-role.name
}

resource "aws_iam_role_policy" "lab-backup-service-pass-role-policy" {
  policy = data.aws_iam_policy_document.lab-pass-role-policy-doc.json
  role   = aws_iam_role.lab-backup-service-role.name
}