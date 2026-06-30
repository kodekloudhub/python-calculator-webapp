// Provisions a Linux Azure App Service that hosts the Python (Flask) calculator app.

@description('Globally-unique web app name. Defaults to a name derived from the resource group id.')
param webAppName string = 'gha-pycalc-${uniqueString(resourceGroup().id)}'

@description('App Service Plan SKU.')
param sku string = 'B1'

@description('Resource location. Defaults to the resource group location.')
param location string = 'westus'

@description('Linux runtime stack for the web app.')
param linuxFxVersion string = 'PYTHON|3.12'

var appServicePlanName = toLower('asp-${webAppName}')

resource appServicePlan 'Microsoft.Web/serverfarms@2022-09-01' = {
  name: appServicePlanName
  location: location
  kind: 'linux'
  properties: {
    reserved: true // required for Linux plans
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
      linuxFxVersion: linuxFxVersion
      // Start the Flask app with gunicorn on the App Service-provided port.
      appCommandLine: 'gunicorn --bind=0.0.0.0:8000 python_calc:app'
      appSettings: [
        {
          // Run an Oryx build (pip install -r requirements.txt) during zip deploy.
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

@description('The name of the provisioned web app (used by the deploy step).')
output webAppName string = appService.name

@description('The default host name of the provisioned web app.')
output webAppHostName string = appService.properties.defaultHostName
