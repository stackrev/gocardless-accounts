from uuid import uuid4

from nordigen import NordigenClient

# initialize Nordigen client and pass SECRET_ID and SECRET_KEY
client = NordigenClient(
    secret_id="ebececbc-7bc9-4e5a-acb3-6a1f7cb67e29",
    secret_key="d03b422065923185f2fe17dbfdd270e2c71a0dcb2e0328cd4c2319e2e2583d9bfce1844e663baf1212584c8f2655589b819d2eab2404380f0c914829c7a4af62"
)

# Create new access and refresh token
# Parameters can be loaded from .env or passed as a string
# Note: access_token is automatically injected to other requests after you successfully obtain it
token_data = client.generate_token()

# Use existing token
# client.token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg2NjU3MDM0LCJqdGkiOiIxOWY0NWQwNDQxMWU0MDFlYjBhZWY5ZjgyMTBlNDcxNCIsImlkIjoyNDE1Mywic2VjcmV0X2lkIjoiZWJlY2VjYmMtN2JjOS00ZTVhLWFjYjMtNmExZjdjYjY3ZTI5IiwiYWxsb3dlZF9jaWRycyI6WyIwLjAuMC4wLzAiLCI6Oi8wIl19.b48mqt5NmVg0PScui_pDkTiikh93irbqYOG20l6olAY"

# Exchange refresh token for new access token
new_token = client.exchange_token(token_data["refresh"])

# Get institution id by bank name and country
institution_id = client.institution.get_institution_id_by_name(
    country="NL",
    institution="Revolut"
)

# Get all institution by providing country code in ISO 3166 format
institutions = client.institution.get_institutions("DE")

# Initialize bank session
init = client.initialize_session(
    # institution id
    institution_id=institution_id,
    # redirect url after successful authentication
    redirect_uri="https://nordigen.com",
    # additional layer of unique ID defined by you
    reference_id=str(uuid4())
)

# Get requisition_id and link to initiate authorization process with a bank
link = init.link # bank authorization link
requisition_id = init.requisition_id



# Get account id after you have completed authorization with a bank
# requisition_id can be gathered from initialize_session response
accounts = client.requisition.get_requisition_by_id(
    requisition_id=init.requisition_id
)

# Get account id from the list.
account_id = accounts["accounts"][0]

# Create account instance and provide your account id from previous step
account = client.account_api(id=account_id)

# Fetch account metadata
meta_data = account.get_metadata()
# Fetch details
details = account.get_details()
# Fetch balances
balances = account.get_balances()
# Fetch transactions
transactions = account.get_transactions()
# Filter transactions by specific date range
transactions = account.get_transactions(date_from="2023-01-01", date_to="2023-05-12")