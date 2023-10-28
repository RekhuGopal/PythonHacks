$cred = Get-Credential

New-AzResourceGroup -Name "Test" -Location "West Europe"

New-AzVm `
    -ResourceGroupName "Test" `
    -Name "VM2122122" `
    -Location "West Europe" `
    -VirtualNetworkName "testvnet" `
    -SubnetName "subnet1" `
    -SecurityGroupName "nsg1" `
    -PublicIpAddressName "iispip" `
    -OpenPorts 80 `
    -Credential $cred

#Set-AzVMExtension -Name AzureMonitorWindowsAgent -ExtensionType AzureMonitorWindowsAgent -Publisher Microsoft.Azure.Monitor -ResourceGroupName "Test" -VMName "myVM2122" -Location "West Europe" -TypeHandlerVersion "1.1" -EnableAutomaticUpgrade $true

New-AzOperationalInsightsWorkspace -Location "West Europe" -Name "TestLAW2122" -Sku PerGB2018 -ResourceGroupName "Test"

New-AzResourceGroupDeployment -ResourceGroupName "Test" -TemplateFile "D:\VSCode\GitRepos\PythonHacks\Azure_VM_Insights\DCR1.json" -TemplateParameterFile "D:\VSCode\GitRepos\PythonHacks\Azure_VM_Insights\DCR1Parameters.json"

$dcr = Get-AzDataCollectionRule -ResourceGroupName "Test" -RuleName "AzVMMonitorRule"
$vmId = '/subscriptions/b048d332-b1ce-4168-95a8-0a48c288e4ef/resourceGroups/Test/providers/Microsoft.Compute/virtualMachines/VM2122122'
New-AzDataCollectionRuleAssociation -TargetResourceId $vmId -AssociationName "dcrAssoc" -RuleId $dcr.Id