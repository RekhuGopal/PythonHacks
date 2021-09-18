# Create Azure RG
resource "azurerm_resource_group" "rg" {
  name = "cloudquickpocscosmosdbrg"
  location = "East US"
}

# Create Azure Cosmos DB Account
resource "azurerm_cosmosdb_account" "acc" {
  name = "cloudquickpocscosmosdbaccount"
  location = "${azurerm_resource_group.rg.location}"
  resource_group_name = "${azurerm_resource_group.rg.name}"
  offer_type = "Standard"
  kind = "GlobalDocumentDB"
  enable_automatic_failover = true
  consistency_policy {
    consistency_level = "Session"
  }

  geo_location {
    location = "West US"
    failover_priority = 1
  }
  geo_location {
    location = "${azurerm_resource_group.rg.location}"
    failover_priority = 0
  }
}

# Azure Cosmos DB database
resource "azurerm_cosmosdb_sql_database" "db" {
  name = "products"
  resource_group_name = "${azurerm_cosmosdb_account.acc.resource_group_name}"
  account_name = "${azurerm_cosmosdb_account.acc.name}"
}

#Azure Cosmos DB database container
resource "azurerm_cosmosdb_sql_container" "coll" {
  name = "Devices"
  resource_group_name = "${azurerm_cosmosdb_account.acc.resource_group_name}"
  account_name = "${azurerm_cosmosdb_account.acc.name}"
  database_name = "${azurerm_cosmosdb_sql_database.db.name}"
  partition_key_path = "/Devices"
}