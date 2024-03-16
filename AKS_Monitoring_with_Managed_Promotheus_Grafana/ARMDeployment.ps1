######################## Prometheus enablement ############################################

# Login to your Azure account
#Connect-AzAccount -UseDeviceAuthentication

# Set variables for resource group and deployment
$resourceGroupName = "cloudquicklabs"
$deploymentName = "managedpromotheus"
$templateFile = "D:\VSCode\GitRepos\PythonHacks\AKS_Monitoring_with_Managed_Promotheus_Grafana\FullAzureMonitorMetricsProfile.json"
$templateParameterFile = "D:\VSCode\GitRepos\PythonHacks\AKS_Monitoring_with_Managed_Promotheus_Grafana\FullAzureMonitorMetricsProfileParameters.json"

$params = @{
      "azureMonitorWorkspaceResourceId"= "/subscriptions/063965e0-d141-48d4-b8bd-0dfdc0dc00ff/resourceGroups/cloudquicklabs/providers/microsoft.monitor/accounts/azmonitorworkspace" 
      "azureMonitorWorkspaceLocation"= "westeurope"
      "clusterResourceId"= "/subscriptions/063965e0-d141-48d4-b8bd-0dfdc0dc00ff/resourcegroups/cloudquicklabs/providers/Microsoft.ContainerService/managedClusters/cloudquicklabsaks"
      "clusterLocation"= "westeurope"
      "metricLabelsAllowlist"= ""
      "metricAnnotationsAllowList"= ""
      "enableWindowsRecordingRules"= $false
      "grafanaResourceId"="/subscriptions/063965e0-d141-48d4-b8bd-0dfdc0dc00ff/resourceGroups/cloudquicklabs/providers/Microsoft.Dashboard/grafana/cloudquicklabsgfana"
      "grafanaLocation"= "westeurope"
      "grafanaSku"= "Standard"
    }

# Deploy the ARM template
New-AzResourceGroupDeployment -Name $deploymentName `
                              -ResourceGroupName $resourceGroupName `
                              -TemplateFile $templateFile `
                              -TemplateParameterObject $params
## Remove deployments
Remove-AzResourceGroupDeployment -Name $deploymentName -ResourceGroupName $resourceGroupName


############################ Container Insights enablement ############################################
$resourceGroupName = "cloudquicklabs"
$deploymentName = "containerinsights"
$templateFile = "D:\VSCode\GitRepos\PythonHacks\AKS_Monitoring_with_Managed_Promotheus_Grafana\ContainerInsightsExistingClusterOnboarding.json"
$templateParameterFile = "D:\VSCode\GitRepos\PythonHacks\AKS_Monitoring_with_Managed_Promotheus_Grafana\ContainerInsightsExistingClusterParam.json"

$params = @{"aksResourceId"= "/subscriptions/063965e0-d141-48d4-b8bd-0dfdc0dc00ff/resourcegroups/cloudquicklabs/providers/Microsoft.ContainerService/managedClusters/cloudquicklabsaks"
            "aksResourceLocation"= "westeurope"
            "workspaceResourceId"= "/subscriptions/063965e0-d141-48d4-b8bd-0dfdc0dc00ff/resourceGroups/cloudquicklabs/providers/Microsoft.OperationalInsights/workspaces/aksInsights"
            "workspaceRegion"= "westeurope"
            "enableContainerLogV2"= $true
            "enableSyslog"= $false
            "syslogLevels"= @( "Debug", "Info", "Notice", "Warning", "Error", "Critical", "Alert", "Emergency" )
           "syslogFacilities"=@(
    "auth",
    "authpriv",
    "cron",
    "daemon",
    "mark",
    "kern",
    "local0",
    "local1",
    "local2",
    "local3",
    "local4",
    "local5",
    "local6",
    "local7",
    "lpr",
    "mail",
    "news",
    "syslog",
    "user",
    "uucp"
  )
"resourceTagValues"= @{
    "evn"= "dev"
    "app"= "sonet"
    "group"= "chees"
  }
"dataCollectionInterval"= "1m"
"namespaceFilteringModeForDataCollection"= "Off"
"namespacesForDataCollection"=@(
    "kube-system",
    "gatekeeper-system",
    "azure-arc"
)
"streams"= @(
    "Microsoft-ContainerLog",
    "Microsoft-ContainerLogV2",
    "Microsoft-KubeEvents",
    "Microsoft-KubePodInventory",
    "Microsoft-KubeNodeInventory",
    "Microsoft-KubePVInventory",
    "Microsoft-KubeServices",
    "Microsoft-KubeMonAgentEvents",
    "Microsoft-InsightsMetrics",
    "Microsoft-ContainerInventory",
    "Microsoft-ContainerNodeInventory",
    "Microsoft-Perf"
  )
"useAzureMonitorPrivateLinkScope"= $false
"azureMonitorPrivateLinkScopeResourceId" = "/subscriptions/063965e0-d141-48d4-b8bd-0dfdc0dc00ff/resourceGroups/cloudquicklabs/providers/microsoft.insights/privateLinkScopes/aksInsights"
}

# Deploy the ARM template
New-AzResourceGroupDeployment -Name $deploymentName `
                          -ResourceGroupName $resourceGroupName `
                          -TemplateFile $templateFile `
                          -TemplateParameterObject $params
