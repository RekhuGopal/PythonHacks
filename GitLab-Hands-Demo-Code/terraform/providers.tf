provider "azurerm" {
  features {}
}

terraform {
  backend "azurerm" {
    resource_group_name  = "costoptimizationsas"
    storage_account_name = "costoptimizationsas1"
    container_name       = "tfstate"
    key                  = "gitlab.tfstate"
  }
}
