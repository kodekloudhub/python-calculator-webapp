// Web app module — provisions a Linux Python Web App.

@description('Resource location.')
param location string

@description('Web app name.')
param webAppName string

@description('App Service Plan SKU.')
param sku string = 'B1'

var appServicePlanName = toLower('asp-${webAppName}')

resource appServicePlan 'Microsoft.Web/serverfarms@2022-09-01' = {
  name: appServicePlanName
  location: location
  kind: 'linux'
  properties: {
    reserved: true
  }
  sku: {
    name: sku
  }
}

resource appService 'Microsoft.Web/sites@2022-09-01' = {
  name: webAppName
  kind: 'app,linux'
  location: location
  properties: {
    serverFarmId: appServicePlan.id
    siteConfig: {
      linuxFxVersion: 'PYTHON|3.12'
      appCommandLine: 'gunicorn --bind=0.0.0.0:8000 python_calc:app'
      appSettings: [
        {
          name: 'SCM_DO_BUILD_DURING_DEPLOYMENT'
          value: 'true'
        }
        {
          name: 'WEBSITES_PORT'
          value: '8000'
        }
      ]
    }
  }
}

output webAppName string = appService.name
output webAppHostName string = appService.properties.defaultHostName
