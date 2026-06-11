# python-calculator-webapp

A small **Python (Flask) calculator** application used across the KodeKloud **AZ-400** labs.
Import this repository into Azure Repos (or use it directly) — each lab uses the pieces it needs.

## Application
| Path | Purpose |
|---|---|
| `python_calc.py` | Flask web calculator (reads optional Azure App Configuration for dynamic title + the `AdvancedOperations` feature flag; falls back to safe defaults) |
| `src/calc.py` | Calculator library (`safe_divide`, `add`, `subtract`, `multiply`) |
| `tests/test_calc.py` | Unit tests (pytest) |
| `requirements.txt` | Python dependencies |
| `Dockerfile`, `docker-compose.yml` | Container build / local compose |

## Infrastructure (`infra/`)
| File | Purpose |
|---|---|
| `webapp.bicep` | Linux Python Web App |
| `webapp-appconfig.bicep` | Web App + `AZURE_APPCONFIG_CONNECTION_STRING` app setting (dynamic config / feature flags lab) |
| `acr.bicep` | Azure Container Registry |
| `webapp-docker.bicep` | Linux Web App for Containers |
| `webapp-to-acr-roleassignment.bicep` | Grants the Web App's managed identity `AcrPull` |
| `appinsights.bicep` | Application Insights + Log Analytics (release-gates lab) |
| `main.bicep` + `modules/` | Modular Bicep (storage + web app) for the Bicep deployments lab |

## Pipelines (`pipelines/`)
| File | Lab |
|---|---|
| `python-calc-docker-ci.yml` / `python-calc-docker-cd.yml` | Deploy Docker containers to Azure App Service |
| `python-multi-stage.yml` | Configure Pipelines as Code with YAML |
| `python-gated-cd.yml` | Control Deployments using Release Gates |
| `python-functional-tests.yml` | Set up and run functional tests |
| `python-keyvault-ci.yml` | Integrate Azure Key Vault |
| `bicep-deploy.yml` | Deployments using Azure Bicep templates |
| `publish-package.yml` | Package Management with Azure Artifacts |

## Other
| Path | Purpose |
|---|---|
| `functional-tests/` | Selenium UI tests (run against the deployed app) |
| `package/` | The `kk-calculator` distributable package (Azure Artifacts lab) |
