#Create RG for function App
resource "azurerm_resource_group" "funcdeploy" {
  name     = "CloudquickPocs-rg-functionApp"
  location = "East US"
}

# Create Azure Storage Account
resource "azurerm_storage_account" "funcdeploy" {
  name                     = "uniquestorageaccount1234"
  resource_group_name      = azurerm_resource_group.funcdeploy.name
  location                 = azurerm_resource_group.funcdeploy.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

# Create azurerm storage container
resource "azurerm_storage_container" "funcdeploy" {
  name                  = "contents"
  storage_account_name  = azurerm_storage_account.funcdeploy.name
  container_access_type = "private"
}

# Create azurerm App insight
resource "azurerm_application_insights" "funcdeploy" {
  name                = "funcapp-appinsights-001"
  location            = azurerm_resource_group.funcdeploy.location
  resource_group_name = azurerm_resource_group.funcdeploy.name
  application_type    = "web"
  tags = {
    "Monitoring" = "functionApp"
  }
}

# Create azurerm app service plan
resource "azurerm_app_service_plan" "funcdeploy" {
  name                = "functions-consumption-asp"
  location            = azurerm_resource_group.funcdeploy.location
  resource_group_name = azurerm_resource_group.funcdeploy.name
  kind                = "FunctionApp"
  reserved            = true

  sku {
    tier = "Dynamic"
    size = "Y1"
  }
}

#Create AzureRM function app
resource "azurerm_function_app" "funcdeploy" {
  name                       = "cloudquickpocsfuncapp"
  location                   = azurerm_resource_group.funcdeploy.location
  resource_group_name        = azurerm_resource_group.funcdeploy.name
  app_service_plan_id        = azurerm_app_service_plan.funcdeploy.id
  storage_account_name       = azurerm_storage_account.funcdeploy.name
  storage_account_access_key = azurerm_storage_account.funcdeploy.primary_access_key
  https_only                 = true
  version                    = "~3"
  os_type                    = "linux"
  app_settings = {
      "WEBSITE_RUN_FROM_PACKAGE" = "1"
      "FUNCTIONS_WORKER_RUNTIME" = "python"
      "APPINSIGHTS_INSTRUMENTATIONKEY" = "${azurerm_application_insights.funcdeploy.instrumentation_key}"
      "APPLICATIONINSIGHTS_CONNECTION_STRING" = "InstrumentationKey=${azurerm_application_insights.funcdeploy.instrumentation_key};IngestionEndpoint=https://japaneast-0.in.applicationinsights.azure.com/"
  }
  site_config {
        linux_fx_version= "Python|3.8"        
        ftps_state = "Disabled"
    }
  identity {
    type = "SystemAssigned"
  }
}