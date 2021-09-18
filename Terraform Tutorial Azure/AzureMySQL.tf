# Create RG
resource "azurerm_resource_group" "mysql" {
  name     = "cloudquickpocsmysql001"
  location = "West US"
}

# My SQL Server
resource "azurerm_mysql_server" "mysql" {
  name                = "cloudquickpoc-mysqlserver"
  location            = azurerm_resource_group.mysql.location
  resource_group_name = azurerm_resource_group.mysql.name

  administrator_login          = "mysqladmin"
  administrator_login_password = "Wegd$##@#!bdv888sa"

  sku_name   = "B_Gen5_2"
  storage_mb = 5120
  version    = "5.7"

  auto_grow_enabled                 = true
  backup_retention_days             = 7
  geo_redundant_backup_enabled      = false
  infrastructure_encryption_enabled = false
  public_network_access_enabled     = true
  ssl_enforcement_enabled           = true
  ssl_minimal_tls_version_enforced  = "TLS1_2"
}

# mysql DB
resource "azurerm_mysql_database" "mysql" {
  name                = "exampledb"
  resource_group_name = azurerm_resource_group.mysql.name
  server_name         = azurerm_mysql_server.mysql.name
  charset             = "utf8"
  collation           = "utf8_unicode_ci"
}

# my sql firewall
resource "azurerm_mysql_firewall_rule" "mysql" {
  name                = "cloudquickpocmysql-fwrules"
  resource_group_name = azurerm_resource_group.mysql.name
  server_name         = azurerm_mysql_server.mysql.name
  start_ip_address    = "0.0.0.0"
  end_ip_address      = "0.0.0.0"
}