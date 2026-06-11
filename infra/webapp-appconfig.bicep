// Linux Python Web App for the feature-flag calculator. The App Configuration connection string
// is supplied as an app setting (AZURE_APPCONFIG_CONNECTION_STRING) so the app can read dynamic
// configuration and feature flags at runtime.

@description('Globally-unique web app name.')
param webAppName string = 'ff-pycalc-${uniqueString(resourceGroup().id)}'

@description('App Service Plan SKU.')
param sku string = 'B1'

@description('Resource location.')
param location string = resourceGroup().location

@description('Azure App Configuration connection string.')
@secure()
param appConfigConnectionString string

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
        {
          name: 'AZURE_APPCONFIG_CONNECTION_STRING'
          value: appConfigConnectionString
        }
      ]
    }
  }
}

output webAppName string = appService.name
output webAppHostName string = appService.properties.defaultHostName
