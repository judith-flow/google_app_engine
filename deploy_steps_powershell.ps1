# if use cloud repository, clone the repository
gcloud source repos clone name_of_the_repository_directory

# go the repository directory
cd directory

# deploy the change in web app 
gcloud app deploy 

# deploy the cron job 
gcloud app deploy cron.yaml 


# Important: 
# when there is any changes in the cron.yaml or the main.py, both app and cron.yaml should be deployed again
