$org = "<OrganizationName>"
$pat = "<PersonalAccessToken>"
$base64AuthInfo = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes(":$pat"))

$response = Invoke-RestMethod `
  -Uri "https://dev.azure.com/$org/_apis/connectionData?api-version=7.1-preview.1" `
  -Headers @{ Authorization = "Basic $base64AuthInfo" }

$response.instanceId