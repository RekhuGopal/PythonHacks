# Create Azure RG
resource "azurerm_resource_group" "IOTHUB" {
  name     = "QuickCloudPOC-RG-IOTHUB"
  location = "East US"
}

# Create Azure Storage Account
resource "azurerm_storage_account" "IOTHUB" {
  name                     = "cloudquickpocsiothub1"
  resource_group_name      = azurerm_resource_group.IOTHUB.name
  location                 = azurerm_resource_group.IOTHUB.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

# Create Azure Storage Account Container
resource "azurerm_storage_container" "IOTHUB" {
  name                  = "iotcontainer"
  storage_account_name  = azurerm_storage_account.IOTHUB.name
  container_access_type = "private"
}

# Create Azure Event Hub Namespace
resource "azurerm_eventhub_namespace" "IOTHUB" {
  name                = "cloudquickiotevthubn"
  resource_group_name = azurerm_resource_group.IOTHUB.name
  location            = azurerm_resource_group.IOTHUB.location
  sku                 = "Basic"
}

# Create Azure Event Hub in Event Hub Namespace
resource "azurerm_eventhub" "IOTHUB" {
  name                = "demoiot-eventhub"
  resource_group_name = azurerm_resource_group.IOTHUB.name
  namespace_name      = azurerm_eventhub_namespace.IOTHUB.name
  partition_count     = 2
  message_retention   = 1
}

# Create Azure event hub authorization rule
resource "azurerm_eventhub_authorization_rule" "IOTHUB" {
  resource_group_name = azurerm_resource_group.IOTHUB.name
  namespace_name      = azurerm_eventhub_namespace.IOTHUB.name
  eventhub_name       = azurerm_eventhub.IOTHUB.name
  name                = "acctest"
  send                = true
}

# Create Azure  IoT HuB
resource "azurerm_iothub" "IOTHUB" {
  name                = "quickcloudpocs-IoTHub"
  resource_group_name = azurerm_resource_group.IOTHUB.name
  location            = azurerm_resource_group.IOTHUB.location

  sku {
    name     = "S1"
    capacity = "1"
  }

  endpoint {
    type                       = "AzureIotHub.StorageContainer"
    connection_string          = azurerm_storage_account.IOTHUB.primary_blob_connection_string
    name                       = "export"
    batch_frequency_in_seconds = 60
    max_chunk_size_in_bytes    = 10485760
    container_name             = azurerm_storage_container.IOTHUB.name
    encoding                   = "Avro"
    file_name_format           = "{iothub}/{partition}_{YYYY}_{MM}_{DD}_{HH}_{mm}"
  }

  endpoint {
    type              = "AzureIotHub.EventHub"
    connection_string = azurerm_eventhub_authorization_rule.IOTHUB.primary_connection_string
    name              = "export2"
  }

  route {
    name           = "export"
    source         = "DeviceMessages"
    condition      = "true"
    endpoint_names = ["export"]
    enabled        = true
  }

  route {
    name           = "export2"
    source         = "DeviceMessages"
    condition      = "true"
    endpoint_names = ["export2"]
    enabled        = true
  }

  tags = {
    purpose = "testing"
  }
}