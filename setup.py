from typing import Optional
import warnings
import subprocess

def load_config():
    config = {
        "resource_group": "lonergan-apis", # change this
        "location": "australiaeast",
        "storage_account": "lrdevdata01", # existing account already owned or a new one
        "function_app": "lonergan-db-api", # change this # azure resource + dns name
        "function_name": "http_endpoint" # function inside the app
    }
    return config

config = load_config()

def check_config_is_valid(login : Optional[bool] = False):
    
    # check group
    res = subprocess.run(["az", "group", "exists", "--name", config["resource_group"]], check=True, capture_output=True, text=True)
    if res.stdout.strip() == "true":
        #raise Exception(f"{res.stdout.strip()}")
        warnings.warn(f"Resource group {config['resource_group']} already exists. Please choose a different name if you want to create a new one.")
    
    res = subprocess.run(
      ["az", "storage", "account", "show",
       "--name", config["storage_account"]],
      capture_output=True, text=True,
    )
    if res.returncode != 0:
        #raise Exception(f"{res.stdout.strip()}")
        warnings.warn(f"Storage account {config['storage_account']} is unavailable.")

def local_setup():
    with open("requirements.txt", "w") as f:
        f.write("azure-functions\n")
        f.write("requests\n")
        f.write("psycopg2-binary\n")
    
    
    subprocess.run(["func", "init", "--python"], check=True)
    
    subprocess.run(["func", "new", "--name", config["function_name"], "--template", "HTTP trigger", "--authlevel", "function"], check=True)
    
    subprocess.run(["python3", "-m", "venv", ".venv"], check=True)
    subprocess.run([".venv/bin/pip", "install", "-r", "requirements.txt"], check=True)
    
def run_local():
    subprocess.run(["func", "start"], check=True)

def see_flex():
    subprocess.run(["az", "functionapp", "list-flexconsumption-locations", "-o", "table"], check=True)
    subprocess.run(
        ["az", "functionapp", "list-flexconsumption-runtimes",
         "--location", config["location"], "--runtime", "python", "-o", "table"],
        check=True,
    )

def az_setup():
    
    #subprocess.run(["az", "login", "--use-device-code"], check=True)
    # TODO : check if resource group exists, if not create it
    res = subprocess.run(["az", "group", "exists", "--name", config["resource_group"]], check=True, capture_output=True, text=True)
    if res.stdout.strip() != "true":
        subprocess.run(["az", "group", "create", "--name", config["resource_group"], "--location", config["location"]], check=True)

    res = subprocess.run(
        ["az", "storage", "account", "show",
         "--name", config["storage_account"],
         "--query", "id", "-o", "tsv"],
        capture_output=True, text=True,
    )
    if res.returncode == 0:
        storage_id = res.stdout.strip()
    else:
        subprocess.run(
            ["az", "storage", "account", "create",
             "--name", config["storage_account"],
             "--resource-group", config["resource_group"],
             "--location", config["location"]],
            check=True,
        )
        res = subprocess.run(
            ["az", "storage", "account", "show",
             "--name", config["storage_account"],
             "--query", "id", "-o", "tsv"],
            check=True, capture_output=True, text=True,
        )
        storage_id = res.stdout.strip()
        
    subprocess.run([
        "az", "functionapp", "create",
        "--name", config["function_app"],
        "--resource-group", config["resource_group"],
        "--storage-account", storage_id,
        "--flexconsumption-location", config["location"],
        "--runtime", "python",
        "--runtime-version", "3.12",
    ], check=True)


def deploy():
    subprocess.run(["func", "azure", "functionapp", "publish", config["function_app"], "--build", "remote"], check=True)

def main():
    local_setup()
    az_setup()
    deploy()

#TODO: args

if __name__ == "__main__":
    main()