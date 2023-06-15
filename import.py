from dotenv import dotenv_values
env_vars = dotenv_values('.env')

import pandas as pd
import json

import http.client

conn = http.client.HTTPSConnection("bankaccountdata.gocardless.com")

payload = ''
headers = {
  'Accept': 'application/json',
  'Authorization': f'Bearer {env_vars["ACCESS_TOKEN"]}'
}
all_transactions = []

accounts = [  
    {
        "institution": "Revolut",
        "id": "4ed83de0-935e-418f-a327-bf229ea4234f",
    },
    {
        "institution": "Revolut",
        "id": "63b94c05-b2c1-4f87-9d7a-b0a01a28ec4c",
    },
    {
        "institution": "Revolut",
        "id": "94ffecf2-e1c1-42cb-911d-8f6412eb6b4f",
    },
    {
        "institution": "Revolut",
        "id": "96527fec-c8bb-4ec4-b983-2af0fd742944",
    },
    {
        "institution": "Revolut",
        "id": "f09fd716-217d-4a88-bfef-e58b61cc0138",
    },
    {
        "institution": "Inteligo",
        "id": "3f6b95a6-32ee-4fc6-a9f6-86f336751f56",
    },
    {
        "institution": "Inteligo",
        "id": "454f3dd6-032e-4856-baab-b249937e4005",
    },
    {
        "institution": "Inteligo",
        "id": "e71eca26-1857-4a87-9071-1568dc13002d"
    }
]
for account in accounts:
  conn.request("GET", f"/api/v2/accounts/{account['id']}/transactions/?date_from=2000-01-01&date_to=2023-06-14", payload, headers)
  res = conn.getresponse()
  data = res.read()

  transactions = json.loads(data)['transactions']

  # Iterate over the "booked" transactions
  for booked_transaction in transactions['booked']:
      transaction_id = booked_transaction["transactionId"]
      booked_transaction['accountId'] = account['id']
      booked_transaction['institution'] = account['institution']
      booked_transaction['status'] = "booked"
      all_transactions.append(booked_transaction)

  # Iterate over the "pending" transactions
  for booked_transaction in transactions['pending']:
      transaction_id = booked_transaction["transactionId"]
      booked_transaction['accountId'] = account['id']
      booked_transaction['institution'] = account['institution']
      booked_transaction['status'] = "pending"
      all_transactions.append(booked_transaction)
  print(f"obtaining for {account['id']} is done")

# Convert the JSON data to a pandas DataFrame
df = pd.DataFrame(all_transactions)

# Define the output file path
output_file = 'transactions.xlsx'

# Write the DataFrame to an XLSX file
df.to_excel(output_file, index=False)

print(f"Data written to {output_file}")