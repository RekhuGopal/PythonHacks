# Create Azure RG
resource "azurerm_resource_group" "ASR" {
  name     = "cloudquickpocs-asr-rg"
  location = "West US"
}

# Create Azure Site Recovery Vault
resource "azurerm_recovery_services_vault" "ASR" {
  name                = "cloudquickpocs-asr-001"
  location            = azurerm_resource_group.ASR.location
  resource_group_name = azurerm_resource_group.ASR.name
  sku                 = "Standard"
}

#  Create Azure Site Recovery Vault VM backup policy
resource "azurerm_backup_policy_vm" "ASR" {
  name                = "cloudquickpocs-asr-vm-policy"
  resource_group_name = azurerm_resource_group.ASR.name
  recovery_vault_name = azurerm_recovery_services_vault.ASR.name

  timezone = "UTC"

  backup {
    frequency = "Daily"
    time      = "23:00"
  }

  retention_daily {
    count = 10
  }

  retention_weekly {
    count    = 42
    weekdays = ["Sunday", "Wednesday", "Friday", "Saturday"]
  }

  retention_monthly {
    count    = 7
    weekdays = ["Sunday", "Wednesday"]
    weeks    = ["First", "Last"]
  }

  retention_yearly {
    count    = 77
    weekdays = ["Sunday"]
    weeks    = ["Last"]
    months   = ["January"]
  }
}