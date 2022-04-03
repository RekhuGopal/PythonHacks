locals {
  backups = {
    schedule  = "cron(0 5 ? * MON-FRI *)" /* UTC Time */
    retention = 7 // days
  }
}

resource "aws_backup_vault" "lab-backup-vault" {
  name = "lab-backup-vault"
  tags = {
    Project = "CloudQuickLabsDemo"
    Role    = "backup-vault"
  }
}

resource "aws_backup_plan" "lab-backup-plan" {
  name = "lab-backup-plan"

  rule {
    rule_name         = "weekdays-every-2-hours-${local.backups.retention}-day-retention"
    target_vault_name = aws_backup_vault.lab-backup-vault.name
    schedule          = local.backups.schedule
    start_window      = 60
    completion_window = 300

    lifecycle {
      delete_after = local.backups.retention
    }

    recovery_point_tags = {
      Project = "CloudQuickLabsDemo"
      Role    = "backup"
      Creator = "aws-backups"
    }
  }

  tags = {
    Project = "CloudQuickLabsDemo"
    Role    = "backup"
  }
}


data "aws_iam_role" "example" {
  name = "ExampleAWSBackupServiceRole"
}


resource "aws_backup_selection" "lab-server-backup-selection" {
  iam_role_arn = data.aws_iam_role.example.arn
  name         = "lab-server-resources"
  plan_id      = aws_backup_plan.lab-backup-plan.id

  selection_tag {
    type  = "STRINGEQUALS"
    key   = "Backup"
    value = "true"
  }
}

