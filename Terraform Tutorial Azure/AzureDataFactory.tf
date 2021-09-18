# Create Azure RG
resource "azurerm_resource_group" "QuickCloudPOCsADF" {
  name     = "QuickCloudPOCsADF-RG"
  location = "northeurope"
}

# Create Azure Data factory
resource "azurerm_data_factory" "QuickCloudPOCsADF" {
  name                = "QuickCloudPOCsADF"
  location            = azurerm_resource_group.QuickCloudPOCsADF.location
  resource_group_name = azurerm_resource_group.QuickCloudPOCsADF.name
}

# Create ADF linked web services
resource "azurerm_data_factory_linked_service_web" "QuickCloudPOCsADF" {
  name                = "QuickCloudPOCsADFlinkedservice"
  resource_group_name = azurerm_resource_group.QuickCloudPOCsADF.name
  data_factory_name   = azurerm_data_factory.QuickCloudPOCsADF.name
  authentication_type = "Anonymous"
  url                 = "https://www.bing.com"
}

# Create ADF data set http
resource "azurerm_data_factory_dataset_http" "QuickCloudPOCsADF" {
  name                = "QuickCloudPOCsADFDataSet"
  resource_group_name = azurerm_resource_group.QuickCloudPOCsADF.name
  data_factory_name   = azurerm_data_factory.QuickCloudPOCsADF.name
  linked_service_name = azurerm_data_factory_linked_service_web.QuickCloudPOCsADF.name

  relative_url   = "http://www.bing.com"
  request_body   = "foo=bar"
  request_method = "POST"
}