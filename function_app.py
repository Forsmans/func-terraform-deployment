import azure.functions as func
import os
import logging
from git import Repo

app = func.FunctionApp()

@app.function_name(name="DeployTerraform")
@app.route(route="deploy", methods=["GET", "POST"])
def deploy_terraform(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")

    # Get repo URL from request
    repo_url = req.params.get("repo_url")
    if not repo_url:
        return func.HttpResponse("Please pass a repo_url on the query string", status_code=400)

    repo_dir = "/tmp/terraform-repo"

    # Remove existing repo if needed
    if os.path.exists(repo_dir):
        logging.info(f"Removing existing directory: {repo_dir}")
        import shutil
        shutil.rmtree(repo_dir)

    # Clone repository using GitPython
    try:
        logging.info(f"Cloning repository: {repo_url}")
        Repo.clone_from(repo_url, repo_dir)
    except Exception as e:
        logging.error(f"Failed to clone repository: {str(e)}")
        return func.HttpResponse(f"Failed to clone repository: {str(e)}", status_code=500)

    # Change directory
    os.chdir(repo_dir)
    logging.info(f"Changed directory to: {repo_dir}")

    # Initialize and apply Terraform
    try:
        logging.info("Initializing Terraform...")
        os.system("terraform init")
        logging.info("Applying Terraform configuration...")
        os.system("terraform apply -auto-approve")
    except Exception as e:
        logging.error(f"Terraform apply failed: {str(e)}")
        return func.HttpResponse(f"Terraform apply failed: {str(e)}", status_code=500)

    logging.info("Terraform apply completed successfully!")
    return func.HttpResponse("Terraform apply completed successfully!", status_code=200)
