#!/bin/bash

# Load variables
source ./variables.sh

# Login to Azure (if not already logged in)
#az login

# Create a resource group
echo "Creating resource group: $RESOURCE_GROUP_NAME"
az group create --name "$RESOURCE_GROUP_NAME" --location "$LOCATION"

# Create a storage account
echo "Creating storage account: $STORAGE_ACCOUNT_NAME"
az storage account create \
  --name "$STORAGE_ACCOUNT_NAME" \
  --location "$LOCATION" \
  --resource-group "$RESOURCE_GROUP_NAME" \
  --sku Standard_LRS

# Create the Function App (Linux-based)
echo "Creating Linux-based Function App: $FUNCTION_APP_NAME"
az functionapp create \
  --name "$FUNCTION_APP_NAME" \
  --storage-account "$STORAGE_ACCOUNT_NAME" \
  --consumption-plan-location "$LOCATION" \
  --resource-group "$RESOURCE_GROUP_NAME" \
  --runtime python \
  --runtime-version 3.10 \
  --functions-version 4 \
  --os-type Linux

# Configure GitHub authentication (if using a private repo)
if [ -n "$GITHUB_TOKEN" ]; then
  echo "Configuring GitHub authentication"
  az functionapp config appsettings set \
    --name "$FUNCTION_APP_NAME" \
    --resource-group "$RESOURCE_GROUP_NAME" \
    --settings "GITHUB_TOKEN=$GITHUB_TOKEN"
fi

# Deploy the function code
echo "Deploying function code"
func azure functionapp publish "$FUNCTION_APP_NAME"

# Configure the startup script
echo "Configuring startup script"
az functionapp config appsettings set \
  --name "$FUNCTION_APP_NAME" \
  --resource-group "$RESOURCE_GROUP_NAME" \
  --settings "STARTUP_COMMAND=bash /home/site/wwwroot/startup.sh"

# Restart the Function App to apply changes
echo "Restarting Function App"
az functionapp restart --name "$FUNCTION_APP_NAME" --resource-group "$RESOURCE_GROUP_NAME"

echo "Function App setup complete!"