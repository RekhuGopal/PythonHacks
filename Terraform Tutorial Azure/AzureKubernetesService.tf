# Local variable
locals {
  aks_cluster_name    = "aks-${local.resource_group_name}"
  location            = "centralus"
  resource_group_name = "CloudQuickPOCsRG001"
}

# Get random
resource "random_pet" "aks_random_1" {}

# Create RG
resource "azurerm_resource_group" "aks_rg_1" {
  location = local.location
  name     = local.resource_group_name
}

# Create Log Analytics Workspace
resource "azurerm_log_analytics_workspace" "aks_law_1" {
  name                = "logs-${random_pet.aks_random_1.id}"
  location            = azurerm_resource_group.aks_rg_1.location
  resource_group_name = azurerm_resource_group.aks_rg_1.name
  retention_in_days   = 30
}

# Aks version
data "azurerm_kubernetes_service_versions" "current" {
  location = azurerm_resource_group.aks_rg_1.location
}

# AKS cluster
resource "azurerm_kubernetes_cluster" "aks_cluster_1" {
  dns_prefix          = local.aks_cluster_name
  kubernetes_version  = data.azurerm_kubernetes_service_versions.current.latest_version
  location            = azurerm_resource_group.aks_rg_1.location
  name                = local.aks_cluster_name
  node_resource_group = "${azurerm_resource_group.aks_rg_1.name}-aks"
  resource_group_name = azurerm_resource_group.aks_rg_1.name

  addon_profile {
    azure_policy { enabled = true }
    oms_agent {
      enabled                    = true
      log_analytics_workspace_id = azurerm_log_analytics_workspace.aks_law_1.id
    }
  }

  default_node_pool {
    availability_zones   = [1]
    enable_auto_scaling  = true
    max_count            = 3
    min_count            = 1
    name                 = "system"
    orchestrator_version = data.azurerm_kubernetes_service_versions.current.latest_version
    os_disk_size_gb      = 1024
    vm_size              = "Standard_DS2_v2"
  }

  identity { type = "SystemAssigned" }

  role_based_access_control {
    enabled = true
    azure_active_directory {
      managed                = true
      admin_group_object_ids = ["4188a639-d87a-437f-ba46-16d706088e20"]
    }
  }
}

# user node pools for - high performance and high availability
resource "azurerm_kubernetes_cluster_node_pool" "usernodepool" {
  availability_zones    = [1]
  enable_auto_scaling   = true
  kubernetes_cluster_id = azurerm_kubernetes_cluster.aks_cluster_1.id
  max_count             = 3
  min_count             = 1
  mode                  = "User"
  name                  = "user"
  orchestrator_version  = data.azurerm_kubernetes_service_versions.current.latest_version
  os_disk_size_gb       = 1024
  vm_size               = "Standard_DS2_v2"
}