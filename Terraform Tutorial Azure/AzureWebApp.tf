# Create a Resource Group
resource "azurerm_resource_group" "appservice-rg" {
  name     = "CloudQuickPoCs-RG001"
  location = "West US"
  tags = {
    description = "POCs Demo"
    environment = "POC"
    owner       = "CloudQuickPoCs"  
  }
}

# Create the App Service Plan
resource "azurerm_app_service_plan" "service-plan" {
  name                = "CloudQuickPoCs-Linux-service-plan-001"
  location            = azurerm_resource_group.appservice-rg.location
  resource_group_name = azurerm_resource_group.appservice-rg.name
  kind                = "Linux"
  reserved            = true

  sku {
    tier = "Standard"
    size = "S1"
  }

  tags = {
    description = "POCs Demo"
    environment = "POC"
    owner       = "CloudQuickPoCs"  
  }
}

# Create the App Service
resource "azurerm_app_service" "app-service" {
  name                = "CloudQuickPoCs-Web-app-service-001"
  location            = azurerm_resource_group.appservice-rg.location
  resource_group_name = azurerm_resource_group.appservice-rg.name
  app_service_plan_id = azurerm_app_service_plan.service-plan.id

  site_config {
    linux_fx_version = "DOTNETCORE|3.1"
  }

  tags = {
    description = "POCs Demo"
    environment = "POC"
    owner       = "CloudQuickPoCs"  
  }
}