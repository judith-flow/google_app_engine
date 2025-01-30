# google_app_engine
deploy cron jobs to load data from aws to gcp
## app.yaml 
it is necessary for app engine service, defines all the environment variables

## batch_ingest.py
generate csv files of the data retrieved through queries and upload into cloud storage

## cron.yaml
define the schedule of the cron jobs 

## requirements.txt
define package dependencies. 
watch out the depreciation. 
if no version is definied, then the latest version will be called. 

## deploy_steps_powershell.ps1
steps and codes for deploying in powershell. 
