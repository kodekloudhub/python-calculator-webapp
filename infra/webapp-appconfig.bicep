// Linux Python Web App for the dynamic-configuration / feature-flags lab.
// After deployment the lab creates an Azure App Configuration store and sets the
// AZURE_APPCONFIG_CONNECTION_STRING app setting on this Web App, so the app reads dynamic
// configuration and feature flags from the store at runtime.

@description('Globally-unique web app name.')
param webAppName string = 'ff-pycalc-${uniqueString(resourceGroup().id)}'

@description('App Service Plan SKU.')
param sku string = 'B1'

@description('Resource location.')
param location string = resourceGroup().location

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
