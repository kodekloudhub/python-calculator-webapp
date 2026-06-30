// main.bicep — top-level template for the calculator's infrastructure.
//
// The Web App is already provisioned through a reusable module (modules/webapp.bicep). The storage
// account is still defined INLINE below. In this lab you will modularize the storage account too
// (extract it into modules/storage.bicep and reference it as a module), then deploy through the
// pipeline.

@description('Resource location. Defaults to the resource group location.')
param location string = 'westus'

@description('Suffix used to build unique resource names.')
param suffix string = uniqueString(resourceGroup().id)

@description('App Service Plan SKU.')
param sku string = 'B1'

// Storage account — defined inline. You will extract this into modules/storage.bicep.
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: 'st${take(suffix, 16)}'
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    minimumTlsVersion: 'TLS1_2'
    allowBlobPublicAccess: false
    supportsHttpsTrafficOnly: true
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
