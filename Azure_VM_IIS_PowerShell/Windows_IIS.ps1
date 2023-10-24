$cred = Get-Credential

New-AzVm `
    -ResourceGroupName "Test" `
    -Name "myVM" `
    -Location "West Europe" `
    -VirtualNetworkName "testvnet" `
    -SubnetName "subnet1" `
    -SecurityGroupName "nsg1" `
    -PublicIpAddressName "iispip" `
    -OpenPorts 80 `
    -Credential $cred


Set-AzVMExtension `
    -ResourceGroupName "Test" `
    -ExtensionName "IIS" `
    -VMName "myVM" `
    -Location "West Europe" `
    -Publisher Microsoft.Compute `
    -ExtensionType CustomScriptExtension `
    -TypeHandlerVersion 1.8 `
    -SettingString '{"commandToExecute":"powershell Add-WindowsFeature Web-Server; powershell Add-Content -Path \"C:\\inetpub\\wwwroot\\Default.htm\" -Value $($env:computername)"}'

Get-AzPublicIPAddress `
    -ResourceGroupName "Test" `
    -Name "iispip" | Select-Object IpAddress