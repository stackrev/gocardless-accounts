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
        "id": "e71eca26-1857-4a87-9071-1568dc13002d"
    },
    {
        "institution": "Inteligo",
        "id": "454f3dd6-032e-4856-baab-b249937e4005",
    },
    {
        "institution": "Inteligo",
        "id": "3f6b95a6-32ee-4fc6-a9f6-86f336751f56",
    },
]
for account in accounts:
  conn.request("GET", f"/api/v2/accounts/{account['id']}/transactions/?date_from=2020-01-01&date_to=2023-06-19", payload, headers)
  res = conn.getresponse()
  data = res.read()

  transactions = json.loads(data)['transactions']

  # Iterate over the "booked" transactions
  for booked_transaction in transactions['booked']:
      transaction_id = booked_transaction["transactionId"]
      booked_transaction['accountId'] = account['id']
      booked_transaction['institution'] = account['institution']
      temp_booked_transaction = booked_transaction['transactionAmount']
      booked_transaction['transactionAmount'] = temp_booked_transaction['amount']
      booked_transaction['transactionCurrency'] = temp_booked_transaction['currency']
      if 'remittanceInformationUnstructuredArray' in booked_transaction:
        booked_transaction['remittanceInformationUnstructuredArray'] = ' '.join(booked_transaction['remittanceInformationUnstructuredArray'])[1:-1]
      if 'currencyExchange' in booked_transaction:
        temp_currency_exchange = booked_transaction['currencyExchange']
        booked_transaction['instructedAmount'] = temp_currency_exchange['instructedAmount']['amount']
        booked_transaction['instructedCurrency'] = temp_currency_exchange['instructedAmount']['currency']
        booked_transaction['sourceCurrency'] = temp_currency_exchange['sourceCurrency']
        booked_transaction['exchangeRate'] = temp_currency_exchange['exchangeRate']
        booked_transaction['unitCurrency'] = temp_currency_exchange['unitCurrency']
        booked_transaction['exchangeRate'] = temp_currency_exchange['exchangeRate']
        booked_transaction['targetCurrency'] = temp_currency_exchange['targetCurrency']
        booked_transaction.pop('currencyExchange')
      booked_transaction['status'] = "booked"
      all_transactions.append(booked_transaction)

  # Iterate over the "pending" transactions
  for booked_transaction in transactions['pending']:
      transaction_id = booked_transaction["transactionId"]
      booked_transaction['accountId'] = account['id']
      booked_transaction['institution'] = account['institution']
      temp_booked_transaction = booked_transaction['transactionAmount']
      booked_transaction['transactionAmount'] = temp_booked_transaction['amount']
      booked_transaction['transactionCurrency'] = temp_booked_transaction['currency']
      booked_transaction['remittanceInformationUnstructuredArray'] = ' '.join(booked_transaction['remittanceInformationUnstructuredArray'])[1:-1]
      if 'currencyExchange' in booked_transaction:
        temp_currency_exchange = booked_transaction['currencyExchange']
        booked_transaction['instructedAmount'] = temp_currency_exchange['instructedAmount']['amount']
        booked_transaction['instructedCurrency'] = temp_currency_exchange['instructedAmount']['currency']
        booked_transaction['sourceCurrency'] = temp_currency_exchange['sourceCurrency']
        booked_transaction['exchangeRate'] = temp_currency_exchange['exchangeRate']
        booked_transaction['unitCurrency'] = temp_currency_exchange['unitCurrency']
        booked_transaction['exchangeRate'] = temp_currency_exchange['exchangeRate']
        booked_transaction['targetCurrency'] = temp_currency_exchange['targetCurrency']
        booked_transaction.pop('currencyExchange')
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