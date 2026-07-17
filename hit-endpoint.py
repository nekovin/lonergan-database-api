import requests
import os
from dotenv import load_dotenv

load_dotenv()

respondent_id = os.getenv("TEST_RESPONDENT")
database_id = os.getenv("DATABASE_ID")
code = os.getenv("CODE")

url = "https://lonergan-db-api.azurewebsites.net/api/remove_number_from_cati"
params = {
    "respondent_id": str(respondent_id),
    "database_id": str(database_id),
    "code": str(code),  # required by auth_level=FUNCTION
}

print(params)

response = requests.get(url, params=params)
print("After hitting...")
print(response.status_code, response.text)
