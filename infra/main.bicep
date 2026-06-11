// main.bicep — top-level template that composes reusable modules to deploy the calculator's
// infrastructure: a storage account and a Linux Python Web App.

@description('Resource location. Defaults to the resource group location.')
param location string = resourceGroup().location

@description('Suffix used to build unique resource names.')
param suffix string = uniqueString(resourceGroup().id)

@description('App Service Plan SKU.')
param sku string = 'B1'

module storage 'modules/storage.bicep' = {
  name: 'storageDeploy'
  params: {
    location: location
    storageAccountName: 'st${take(suffix, 16)}'
  }
}

module web 'modules/webapp.bicep' = {
  name: 'webDeploy'
  params: {
    location: location
    webAppName: 'bicep-pycalc-${suffix}'
    sku: sku
  }
}

output webAppName string = web.outputs.webAppName
output webAppHostName string = web.outputs.webAppHostName
output storageAccountName string = storage.outputs.storageAccountName
