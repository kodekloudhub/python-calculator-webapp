# python-calculator-webapp

A small **Python (Flask) calculator** application used across the KodeKloud **AZ-400** labs.
Import this repository into Azure Repos (or use it directly) — each lab uses the pieces it needs.

## Application
| Path | Purpose |
|---|---|
| `python_calc.py` | Flask web calculator (reads optional Azure App Configuration via `AZURE_APPCONFIG_CONNECTION_STRING` for a dynamic banner + the `SalesWeekend` feature flag; falls back to safe defaults) |
| `src/calc.py` | Calculator library (`safe_divide`, `add`, `subtract`, `multiply`) |
| `tests/test_calc.py` | Unit tests (pytest) |
| `requirements.txt` | Python dependencies |
| `Dockerfile`, `docker-compose.yml` | Container build / local compose |

## Infrastructure (`infra/`)
| File | Purpose |
|---|---|
| `webapp.bicep` | Linux Python Web App |
| `webapp-appconfig.bicep` | Linux Python Web App for the dynamic config / feature flags lab (connection string set post-deploy) |
| `acr.bicep` | Azure Container Registry |
| `webapp-docker.bicep` | Linux Web App for Containers |
| `webapp-to-acr-roleassignment.bicep` | Grants the Web App's managed identity `AcrPull` |
| `main.bicep` + `modules/webapp.bicep` | Bicep deployments lab — `main.bicep` uses the web app module and has the storage account inline; the lab walks you through extracting `modules/storage.bicep` |

## Pipelines (`pipelines/`)
| File | Lab |
|---|---|
| `python-calc-docker-ci.yml` / `python-calc-docker-cd.yml` | Deploy Docker containers to Azure App Service |
| `python-multi-stage.yml` | Configure Pipelines as Code with YAML |
| `python-calc-ci.yml` | Release Gates + Dynamic Configuration labs (CI: build + publish the `Website` artifact) |
| `python-functional-tests.yml` | Set up and run functional tests |
| `python-calc-ci-dockercompose.yml` / `python-calc-cd-aci.yml` | Integrate Azure Key Vault (Docker Compose CI / ACI CD) |
| `python-calc-cd-appconfig.yml` | Enable Dynamic Configuration and Feature Flags (CD: deploy the Web App, triggered by `python-calc-ci`) |
| `bicep-deploy.yml` | Deployments using Azure Bicep templates |
| `publish-package.yml` | Package Management with Azure Artifacts |

## Other
| Path | Purpose |
|---|---|
| `functional-tests/` | Selenium UI tests (run against the deployed app) |
| `package/` | The `kk-calculator` distributable package (Azure Artifacts lab) |
