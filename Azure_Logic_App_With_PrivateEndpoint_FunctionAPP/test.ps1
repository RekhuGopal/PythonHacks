az login --use-device-code

# variables.
$resourceGroupName = "MyLogicAppRGTest"
$vnetName = "LogicAppNetTest"
$subnetName = "LogicAppSubTest"
$region = "eastus"

# Create a resource resourceGroupName
az group create --name "$resourceGroupName" --location "$region"

# Create a new Vnet
az network vnet create `
  --name "$vnetName" `
  --resource-group "$resourceGroupName" `
  --address-prefixes 10.2.0.0/16 `
  --subnet-name "$subnetName" `
  --subnet-prefixes 10.2.0.0/24
  
# Create Private DNS Zone
az network private-dns zone create `
    --resource-group "$resourceGroupName" `
    --name "privatelink.azurewebsites.net"

# Link Private DNS Zone with VNET
az network private-dns link vnet create `
    --resource-group "$resourceGroupName" `
    --name "$vnetName-DNS-Link" `
    --zone-name "privatelink.azurewebsites.net" `
    --virtual-network "$vnetName" `
    --registration-enabled "true"