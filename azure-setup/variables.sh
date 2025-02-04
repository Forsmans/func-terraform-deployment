# variables.sh

# Resource Group
RESOURCE_GROUP_NAME="my-func-rg"
LOCATION="westeurope"

# Storage Account (must be globally unique)
STORAGE_ACCOUNT_NAME="xenitmffuncstorage$RANDOM"

# Function App (must be globally unique)
FUNCTION_APP_NAME="func-pipeline-$RANDOM"

# GitHub Repository
GITHUB_REPO_URL="https://github.com/Forsmans/terraform-rg.git"

# GitHub Personal Access Token (for private repos)
GITHUB_TOKEN=""
