@description('Generate a Suffix based on the Resource Group ID')
param suffix string = uniqueString(resourceGroup().id)

@description('Use the Resource Group Location')
param location string = resourceGroup().location

// Reference the existing Azure Container Registry. Its admin user is enabled by the CD pipeline
// before this template is deployed, so listCredentials() returns the registry username/password.
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

// Web App for Containers. It pulls the image using the ACR admin credentials supplied as
// DOCKER_REGISTRY_SERVER_* app settings (the sandbox disallows the AcrPull role assignment a
// managed identity would otherwise need).
resource webApp 'Microsoft.Web/sites@2022-03-01' = {
  name: 'app-${suffix}'
  location: location
  properties: {
    serverFarmId: appServicePlan.id
    siteConfig: {
      linuxFxVersion: 'DOCKER|${acr.properties.loginServer}/web:latest'
      appSettings: [
        {
          name: 'WEBSITES_PORT'
          value: '80'
        }
        {
          name: 'UseOnlyInMemoryDatabase'
          value: 'true'
        }
        {
          name: 'DOCKER_REGISTRY_SERVER_URL'
          value: 'https://${acr.properties.loginServer}'
        }
        {
          name: 'DOCKER_REGISTRY_SERVER_USERNAME'
          value: acr.listCredentials().username
        }
        {
          name: 'DOCKER_REGISTRY_SERVER_PASSWORD'
          value: acr.listCredentials().passwords[0].value
        }
      ]
    }
  }
}
