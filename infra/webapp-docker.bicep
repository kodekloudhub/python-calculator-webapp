@description('Generate a Suffix based on the Resource Group ID')
param suffix string = uniqueString(resourceGroup().id)

@description('Use the Resource Group Location')
param location string = resourceGroup().location

// Reference existing Azure Container Registry
resource acr 'Microsoft.ContainerRegistry/registries@2021-09-01' existing = {
  name: 'cr${suffix}'
}

// App Service Plan
resource appServicePlan 'Microsoft.Web/serverfarms@2022-03-01' = {
  name: 'asp-${suffix}'
  location: location
  kind: 'linux'
  properties: {
    reserved: true
  }
  sku: {
    name: 'B1'
  }
}

// Web App for Python Flask container
resource webApp 'Microsoft.Web/sites@2022-03-01' = {
  name: 'app-${suffix}'
  location: location
  tags: {}
  properties: {
    serverFarmId: appServicePlan.id
    siteConfig: {
      acrUseManagedIdentityCreds: true
      linuxFxVersion: 'DOCKER|${acr.properties.loginServer}/web:latest'  // your Python image
      appSettings: [
        {
          name: 'WEBSITES_PORT'
          value: '80'
        }
        {
          name: 'UseOnlyInMemoryDatabase'
          value: 'true'
        }
      ]
    }
  }
  identity: {
    type: 'SystemAssigned'
  }
}
