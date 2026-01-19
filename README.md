# RouteTracker

## Installation
* Setup up Google Cloud for Routing to have an API Key with enabled billing.
* Install Python with venv
* Authenticate using [google-api-core](https://googleapis.dev/python/google-api-core/latest/auth.html) with Google for localhost
* Create file `auto_run_list.py` with a list `export_list` containing the routes to be tracked.
* Create .env file with GOOGLE_API_KEY=""

## Notes
* Create requirements.txt: `pip freeze > requirements.txt`
* Install from requirements: `pip install -r requirements.txt`
* Create venv `python -m venv env`

### auto_run_list
* days of week starts at 0 for Monday

## GCloud Notes
* Authorize service account to "Full Access" (Not sure if necessary)
   * gcloud compute instances set-service-account YOUR_VM_NAME --zone=YOUR_ZONE --scopes=https://www.googleapis.com/auth/cloud-platform