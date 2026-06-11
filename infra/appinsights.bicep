// Application Insights + a metric alert rule used by the release gate.
// The "Query Azure Monitor alerts" gate on the production environment checks whether any
// alert in this resource group is firing before allowing the deployment to proceed.

@description('Use the resource group location.')
param location string = resourceGroup().location

@description('Suffix derived from the resource group id for unique names.')
param suffix string = uniqueString(resourceGroup().id)

resource workspace 'Microsoft.OperationalInsights/workspaces@2022-10-01' = {
  name: 'log-${suffix}'
  location: location
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: 30
  }
}

resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: 'appi-${suffix}'
  location: location
  kind: 'web'
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: workspace.id
  }
}

@description('Output the Application Insights connection string.')
output appInsightsConnectionString string = appInsights.properties.ConnectionString

@description('Output the Application Insights name.')
output appInsightsName string = appInsights.name
