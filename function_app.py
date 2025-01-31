import azure.functions as func
import os
import subprocess
import logging

app = func.FunctionApp()

@app.function_name(name="DeployTerraform")
@app.route(route="deploy", methods=["GET", "POST"])
def deploy_terraform(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Clone the GitHub repository
    repo_url = req.params.get('repo_url')
    if not repo_url:
        return func.HttpResponse("Please pass a repo_url on the query string", status_code=400)

    logging.info(f"Cloning repository: {repo_url}")
    repo_dir = "/tmp/terraform-repo"
    if os.path.exists(repo_dir):
        logging.info(f"Removing existing directory: {repo_dir}")
        subprocess.run(["rm", "-rf", repo_dir], check=True)

    try:
        logging.info("Cloning repository...")
        subprocess.run(["git", "clone", repo_url, repo_dir], check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to clone repository: {str(e)}")
        return func.HttpResponse(f"Failed to clone repository: {str(e)}", status_code=500)

    # Navigate to the repo directory
    os.chdir(repo_dir)
    logging.info(f"Changed directory to: {repo_dir}")

    # Initialize Terraform
    try:
        logging.info("Initializing Terraform...")
        subprocess.run(["terraform", "init"], check=True)
        logging.info("Applying Terraform configuration...")
        subprocess.run(["terraform", "apply", "-auto-approve"], check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Terraform apply failed: {str(e)}")
        return func.HttpResponse(f"Terraform apply failed: {str(e)}", status_code=500)

    logging.info("Terraform apply completed successfully!")
    return func.HttpResponse("Terraform apply completed successfully!", status_code=200)