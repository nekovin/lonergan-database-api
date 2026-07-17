import subprocess

def load_config():
    config = {
        "resource_group": "myResourceGroup", # change this
        "location": "australiaeast",
        "storage_account": "mystorageaccount", # change this
        "function_app": "myFunctionApp", # change this # azure resource + dns name
        "function_name": "myFunctionApp" # change this # function inside the app
    }
    return config

config = load_config()

def local_setup():
    with open("requirements.txt", "w") as f:
        f.write("azure-functions\n")
        f.write("requests\n")
        f.write("psycopg2-binary\n")
    
    
    subprocess.run(["func", "init", "--python"], check=True)
    
    subprocess.run(["func", "new", "--name", config["function_name"], "--template", "HTTP trigger", "--authlevel", "function"], check=True)
    
    subprocess.run(["python", "-m", "venv", ".venv"], check=True)
    subprocess.run([".venv/bin/pip", "install", "-r", "requirements.txt"], check=True)
    
def run_local():
    subprocess.run(["func", "start"], check=True)

def az_setup():
    
    subprocess.run(["az", "login", "--use-device-code"], check=True)
    subprocess.run(["az", "group", "create", "--name", config["resource_group"], "--location", config["location"]], check=True)
    subprocess.run(["az", "storage", "account", "create", "--name", config["storage_account"], "--location", config["location"], "--resource-group", config["resource_group"]], check=True)
    
    subprocess.run([
        "az", "functionapp", "create",
        "--name", config["function_app"],
        "--resource-group", config["resource_group"],
        "--storage-account", config["storage_account"],
        "--consumption-plan-location", config["location"],
        "--runtime", "python",
        "--runtime-version", "3.12",
        "--functions-version", "4",
        "--os-type", "Linux",
    ], check=True)


def deploy():
    subprocess.run(["func", "azure", "functionapp", "publish", config["function_app"]], check=True)

def main():
    local_setup()
    az_setup()
    deploy()

if __name__ == "__main__":
    main()