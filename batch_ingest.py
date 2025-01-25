#!/usr/bin/env python

# [START app]
import os
import logging
import flask
import pymysql
import datetime
import pandas as pd

from google.cloud import storage
from google.cloud.storage import Blob
from google.cloud import secretmanager


# [start config]
app = flask.Flask(__name__)
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
# [end config]

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
secrets = secretmanager.SecretManagerServiceClient()
name_pw = f"projects/{PROJECT_ID}/secrets/cloud_sql_database_pw/versions/1"
name_user = f"projects/{PROJECT_ID}/secrets/cloud_sql_database_user/versions/1"
name_host = f"projects/{PROJECT_ID}/secrets/cloud_sql_database_host/versions/1"
HOST_PW=secrets.access_secret_version(name=name_pw).payload.data.decode("UTF-8")
HOST_USER=secrets.access_secret_version(name=name_user).payload.data.decode("UTF-8")
HOST_NAME=secrets.access_secret_version(name=name_host).payload.data.decode("UTF-8")

#CLOUD KPI
@app.route('/kpi_pricelists')
def kpi_pricelists():
    # verify that this is a cron job request
    is_cron = flask.request.headers['X-Appengine-Cron']
    logging.info('Received cron request {}'.format(is_cron))
    try:
        status = ingest(mode='kpi_pricelists')

    except KeyError as e:
        status = '<html>Sorry, this capability is accessible only by the Cron service, but I got a KeyError for {} -- try invoking it from <a href="{}"> the GCP console / AppEngine / taskqueues </a></html>'.format(e, 'http://console.cloud.google.com/appengine/taskqueues?tab=CRON')
        logging.exception('Rejected non-Cron request')
    return status

@app.route('/kpi_teams')
def kpi_teams():
    # verify that this is a cron job request
    is_cron = flask.request.headers['X-Appengine-Cron']
    logging.info('Received cron request {}'.format(is_cron))
    try:
        status = ingest(mode='kpi_teams')

    except KeyError as e:
        status = '<html>Sorry, this capability is accessible only by the Cron service, but I got a KeyError for {} -- try invoking it from <a href="{}"> the GCP console / AppEngine / taskqueues </a></html>'.format(e, 'http://console.cloud.google.com/appengine/taskqueues?tab=CRON')
        logging.exception('Rejected non-Cron request')
    return status

@app.route('/kpi_forms')
def kpi_forms():
    # verify that this is a cron job request
    is_cron = flask.request.headers['X-Appengine-Cron']
    logging.info('Received cron request {}'.format(is_cron))
    try:
        status = ingest(mode='kpi_forms')

    except KeyError as e:
        status = '<html>Sorry, this capability is accessible only by the Cron service, but I got a KeyError for {} -- try invoking it from <a href="{}"> the GCP console / AppEngine / taskqueues </a></html>'.format(e, 'http://console.cloud.google.com/appengine/taskqueues?tab=CRON')
        logging.exception('Rejected non-Cron request')
    return status

@app.route('/kpi_accounts')
def kpi_accounts():
    # verify that this is a cron job request
    is_cron = flask.request.headers['X-Appengine-Cron']
    logging.info('Received cron request {}'.format(is_cron))
    try:
        status = ingest(mode='kpi_accounts')

    except KeyError as e:
        status = '<html>Sorry, this capability is accessible only by the Cron service, but I got a KeyError for {} -- try invoking it from <a href="{}"> the GCP console / AppEngine / taskqueues </a></html>'.format(e, 'http://console.cloud.google.com/appengine/taskqueues?tab=CRON')
        logging.exception('Rejected non-Cron request')
    return status

#CONVERSION FUNNEL
@app.route('/conversion_funnel')
def conversion_funnel():
    # verify that this is a cron job request
    is_cron = flask.request.headers['X-Appengine-Cron']
    logging.info('Received cron request {}'.format(is_cron))
    try:
        status = ingest(mode='conversion_funnel')

    except KeyError as e:
        status = '<html>Sorry, this capability is accessible only by the Cron service, but I got a KeyError for {} -- try invoking it from <a href="{}"> the GCP console / AppEngine / taskqueues </a></html>'.format(e, 'http://console.cloud.google.com/appengine/taskqueues?tab=CRON')
        logging.exception('Rejected non-Cron request')
    return status

#REFERRALS
@app.route('/referrals')
def referrals():
    # verify that this is a cron job request
    is_cron = flask.request.headers['X-Appengine-Cron']
    logging.info('Received cron request {}'.format(is_cron))
    try:
        status = ingest(mode='referrals')

    except KeyError as e:
        status = '<html>Sorry, this capability is accessible only by the Cron service, but I got a KeyError for {} -- try invoking it from <a href="{}"> the GCP console / AppEngine / taskqueues </a></html>'.format(e, 'http://console.cloud.google.com/appengine/taskqueues?tab=CRON')
        logging.exception('Rejected non-Cron request')
    return status

@app.route('/industries')
def industries():
    # verify that this is a cron job request
    is_cron = flask.request.headers['X-Appengine-Cron']
    logging.info('Received cron request {}'.format(is_cron))
    try:
        status = ingest(mode='industries')

    except KeyError as e:
        status = '<html>Sorry, this capability is accessible only by the Cron service, but I got a KeyError for {} -- try invoking it from <a href="{}"> the GCP console / AppEngine / taskqueues </a></html>'.format(e, 'http://console.cloud.google.com/appengine/taskqueues?tab=CRON')
        logging.exception('Rejected non-Cron request')
    return status

@app.route('/devices')
def devices():
    # verify that this is a cron job request
    is_cron = flask.request.headers['X-Appengine-Cron']
    logging.info('Received cron request {}'.format(is_cron))
    try:
        status = ingest(mode='devices')

    except KeyError as e:
        status = '<html>Sorry, this capability is accessible only by the Cron service, but I got a KeyError for {} -- try invoking it from <a href="{}"> the GCP console / AppEngine / taskqueues </a></html>'.format(e, 'http://console.cloud.google.com/appengine/taskqueues?tab=CRON')
        logging.exception('Rejected non-Cron request')
    return status


#@app.route('/payments_r')
#def payments_r():
    # verify that this is a cron job request
 #   is_cron = flask.request.headers['X-Appengine-Cron']
 #   logging.info('Received cron request {}'.format(is_cron))
 #   try:
 #       status = ingest(mode='payments_r')

#    except KeyError as e:
#        status = '<html>Sorry, this capability is accessible only by the Cron service, but I got a KeyError for {} -- try invoking it from <a href="{}"> the GCP console / AppEngine / taskqueues </a></html>'.format(e, 'http://console.cloud.google.com/appengine/taskqueues?tab=CRON')
#        logging.exception('Rejected non-Cron request')
#    return status 

#REVENUE
@app.route('/payments')
def payments():
    # verify that this is a cron job request
    is_cron = flask.request.headers['X-Appengine-Cron']
    logging.info('Received cron request {}'.format(is_cron))
    try:
        status = ingest(mode='payments')

    except KeyError as e:
        status = '<html>Sorry, this capability is accessible only by the Cron service, but I got a KeyError for {} -- try invoking it from <a href="{}"> the GCP console / AppEngine / taskqueues </a></html>'.format(e, 'http://console.cloud.google.com/appengine/taskqueues?tab=CRON')
        logging.exception('Rejected non-Cron request')
    return status

@app.route('/workgroups')
def workgroups():
    # verify that this is a cron job request
    is_cron = flask.request.headers['X-Appengine-Cron']
    logging.info('Received cron request {}'.format(is_cron))
    try:
        status = ingest(mode='workgroups')

    except KeyError as e:
        status = '<html>Sorry, this capability is accessible only by the Cron service, but I got a KeyError for {} -- try invoking it from <a href="{}"> the GCP console / AppEngine / taskqueues </a></html>'.format(e, 'http://console.cloud.google.com/appengine/taskqueues?tab=CRON')
        logging.exception('Rejected non-Cron request')
    return status

@app.route('/billings')
def billings():
    # verify that this is a cron job request
    is_cron = flask.request.headers['X-Appengine-Cron']
    logging.info('Received cron request {}'.format(is_cron))
    try:
        status = ingest(mode='billings')

    except KeyError as e:
        status = '<html>Sorry, this capability is accessible only by the Cron service, but I got a KeyError for {} -- try invoking it from <a href="{}"> the GCP console / AppEngine / taskqueues </a></html>'.format(e, 'http://console.cloud.google.com/appengine/taskqueues?tab=CRON')
        logging.exception('Rejected non-Cron request')
    return status

@app.route('/subscriptions_revenue')
def subscriptions_revenue():
    # verify that this is a cron job request
    is_cron = flask.request.headers['X-Appengine-Cron']
    logging.info('Received cron request {}'.format(is_cron))
    try:
        status = ingest(mode='subscriptions_revenue')

    except KeyError as e:
        status = '<html>Sorry, this capability is accessible only by the Cron service, but I got a KeyError for {} -- try invoking it from <a href="{}"> the GCP console / AppEngine / taskqueues </a></html>'.format(e, 'http://console.cloud.google.com/appengine/taskqueues?tab=CRON')
        logging.exception('Rejected non-Cron request')
    return status

#INITIAL BY CUSTOMLYTICS
@app.route('/subscriptions')
def subscriptions():
    # verify that this is a cron job request
    is_cron = flask.request.headers['X-Appengine-Cron']
    logging.info('Received cron request {}'.format(is_cron))
    try:
        status = ingest(mode='subscriptions')

    except KeyError as e:
        status = '<html>Sorry, this capability is accessible only by the Cron service, but I got a KeyError for {} -- try invoking it from <a href="{}"> the GCP console / AppEngine / taskqueues </a></html>'.format(e, 'http://console.cloud.google.com/appengine/taskqueues?tab=CRON')
        logging.exception('Rejected non-Cron request')
    return status


@app.route('/users')
def users():
    # verify that this is a cron job request
    is_cron = flask.request.headers['X-Appengine-Cron']
    logging.info('Received cron request {}'.format(is_cron))
    try:
        status = ingest(mode='users')

    except KeyError as e:
        status = '<html>Sorry, this capability is accessible only by the Cron service, but I got a KeyError for {} -- try invoking it from <a href="{}"> the GCP console / AppEngine / taskqueues </a></html>'.format(e, 'http://console.cloud.google.com/appengine/taskqueues?tab=CRON')
        logging.exception('Rejected non-Cron request')
    return status

# SUBSCRIPTIONS_UPDATED
@app.route('/subscriptions_updated')
def subscriptions_updated():
    # verify that this is a cron job request
    is_cron = flask.request.headers['X-Appengine-Cron']
    logging.info('Received cron request {}'.format(is_cron))
    try:
        status = ingest(mode='subscriptions_updated')

    except KeyError as e:
        status = '<html>Sorry, this capability is accessible only by the Cron service, but I got a KeyError for {} -- try invoking it from <a href="{}"> the GCP console / AppEngine / taskqueues </a></html>'.format(e, 'http://console.cloud.google.com/appengine/taskqueues?tab=CRON')
        logging.exception('Rejected non-Cron request')
    return status


# USERS WORKGROUPS
@app.route('/users_workgroups')
def users_workgroups():
    # verify that this is a cron job request
    is_cron = flask.request.headers['X-Appengine-Cron']
    logging.info('Received cron request {}'.format(is_cron))
    try:
        status = ingest(mode='users_workgroups')

    except KeyError as e:
        status = '<html>Sorry, this capability is accessible only by the Cron service, but I got a KeyError for {} -- try invoking it from <a href="{}"> the GCP console / AppEngine / taskqueues </a></html>'.format(e, 'http://console.cloud.google.com/appengine/taskqueues?tab=CRON')
        logging.exception('Rejected non-Cron request')
    return status


@app.route('/api_log_remove')
def api_log_remove():
    # verify that this is a cron job request
    is_cron = flask.request.headers['X-Appengine-Cron']
    logging.info('Received cron request {}'.format(is_cron))
    try:
        status = ingest(mode='api_log_remove')

    except KeyError as e:
        status = '<html>Sorry, this capability is accessible only by the Cron service, but I got a KeyError for {} -- try invoking it from <a href="{}"> the GCP console / AppEngine / taskqueues </a></html>'.format(e, 'http://console.cloud.google.com/appengine/taskqueues?tab=CRON')
        logging.exception('Rejected non-Cron request')
    return status


def ingest(mode):
    status = 'all good'
    logging.info('Start to pull data for: {}'.format(mode))
    try:
        connection = pymysql.connect(host = HOST_NAME,
                                     user = HOST_USER,
                                     password= HOST_PW,
                                     database=os.environ['HOST_DB_NAME'],
                                     port=int(os.environ['HOST_PORT']),
                                     connect_timeout=int(os.environ['HOST_TIMEOUT']))
        # load the right query and set the file name and schema accordingly
        #CLOUD KPI
        if mode == 'kpi_pricelists':
            query = os.environ['QUERY_KPI_PRICELISTS']
            csvfile = 'kpi_pricelists_{}.csv'.format((datetime.datetime.now()).strftime('%Y-%m-%d'))
            schema = ['pricelist_id',
                      'country',
                      'status',
                      'created']
            bucket = os.environ['GS_KPI_PRICELISTS_BUCKET']
        elif mode == 'kpi_teams':
            query = os.environ['QUERY_KPI_TEAMS']
            csvfile = 'kpi_teams_{}.csv'.format((datetime.datetime.now()).strftime('%Y-%m-%d'))
            schema = ['workgroup_id',
                      'type',
                      'created']
            bucket = os.environ['GS_KPI_TEAMS_BUCKET'] 
        elif mode == 'kpi_forms':
            query = os.environ['QUERY_KPI_FORMS']
            csvfile = 'kpi_forms_{}.csv'.format((datetime.datetime.now()).strftime('%Y-%m-%d'))
            schema = ['form_id',
                      'custom_form',
                      'created']
            bucket = os.environ['GS_KPI_FORMS_BUCKET'] 
        elif mode == 'kpi_accounts':
            query = os.environ['QUERY_KPI_ACCOUNTS']
            csvfile = 'kpi_accounts_{}.csv'.format((datetime.datetime.now()).strftime('%Y-%m-%d'))
            schema = ['user_id',
                      'email',
                      'signup_origin',
                      'created']
            bucket = os.environ['GS_KPI_ACCOUNTS_BUCKET'] 
        #CONVERSION FUNNEL
        elif mode == 'conversion_funnel':
            query = os.environ['QUERY_USERS_FUNNEL']
            csvfile = 'users_funnel_{}.csv'.format((datetime.datetime.now()).strftime('%Y-%m-%d'))
            schema = ['id',
                      'email',
                      'signup_origin',
                      'sign_up_date',
                      'country',
                      'marketing_use_case',
                      'marketing_intent']
            bucket = os.environ['GS_USERS_FUNNEL_BUCKET']
        #REFERRALS
        elif mode == 'referrals':
            query = os.environ['QUERY_REFERRALS']
            csvfile = 'referrals_{}.csv'.format((datetime.datetime.now()).strftime('%Y-%m-%d'))
            schema = ['user_id',
                      'created',
                      'referral_code']
            bucket = os.environ['GS_REFERRALS_BUCKET']
        elif mode == 'industries':
            query = os.environ['QUERY_INDUSTRIES']
            csvfile = 'industries_{}.csv'.format((datetime.datetime.now()).strftime('%Y-%m-%d'))
            schema = ['user_id',
                      'industry_name',
                      'created']
            bucket = os.environ['GS_INDUSTRIES_BUCKET']
        elif mode == 'devices':
            query = os.environ['QUERY_DEVICES']
            csvfile = 'devices_{}.csv'.format((datetime.datetime.now()).strftime('%Y-%m-%d'))
            schema = ['user_id',
                      'device_id',
                      'email',
                      'os',
                      'created']                    
            bucket = os.environ['GS_DEVICES_BUCKET']
        #elif mode == 'payments_r':
        #    query = os.environ['QUERY_PAYMENTS_R']
        #    csvfile = 'payments_{}.csv'.format((datetime.datetime.now()).strftime('%Y-%m-%d'))
        #    schema = ['user_id',
        #              'product',
        #              'amount',
        #              'currency',
        #              'payment_date']
        #    bucket = os.environ['GS_PAYMENTS_R_BUCKET']
        #REVENUE    
        elif mode == 'payments':
            query = os.environ['QUERY_PAYMENTS']
            csvfile = 'payments_{}.csv'.format((datetime.datetime.now()).strftime('%Y-%m-%d'))
            schema = ['date',
                      'billing_id',
                      'workgroup_id',
                      'subscription_id',
                      'sensopia_id',
                      'user_id',
                      'email',
                      'amount',
                      'fee',
                      'currency',
                      'payment_status',
                      'item_number',
                      'item_name',
                      'creator',
                      'created',
                      'start_date', 
                      'end_date']
            bucket = os.environ['GS_PAYMENTS_BUCKET']
        elif mode == 'workgroups':
            query = os.environ['QUERY_WORKGROUPS']
            csvfile = 'workgroups_{}.csv'.format((datetime.datetime.now()).strftime('%Y-%m-%d'))
            schema = ['workgroup_id',
                      'admin',
                      'owner',
                      'type',
                      'created',
                      'modified',
                      'parent_id',
                      'sensopia_id',
                      'admin_id',
                      'owner_id']
            bucket = os.environ['GS_WORKGROUPS_BUCKET']
        elif mode == 'billings':
            query = os.environ['QUERY_BILLINGS']
            csvfile = 'billings_status_{}.csv'.format((datetime.datetime.now()).strftime('%Y-%m-%d'))
            schema = ['billing_id',
                      'sensopia_id',
                      'workgroup_id',
                      'user_id',
                      'creator',
                      'billing_cycle',
                      'creation_date',
                      'expiration_date',
                      'snapshot_date']
            bucket = os.environ['GS_BILLINGS_BUCKET']
        elif mode == 'subscriptions_revenue':
            query = os.environ['QUERY_SUBSCRIPTIONS_REVENUE']
            csvfile = 'subscriptions_revenue_{}.csv'.format((datetime.datetime.now()).strftime('%Y-%m-%d'))
            schema = ['subscription_id',
                      'email',
                      'sensopia_id',
                      'billing_id',
                      'workgroup_id',
                      'created',
                      'modified']
            bucket = os.environ['GS_SUBSCRIPTIONS_REVENUE_BUCKET']
        #INITIAL BY CUSTOMLYTICS
        elif mode == 'subscriptions':
            query = os.environ['QUERY_SUBSCRIPTIONS']
            csvfile = 'subscriptions_{}.csv'.format((datetime.datetime.now()).strftime('%Y-%m-%d'))
            schema = ['user_id',
                      'sensopia_id',
                      'assigned_to',
                      'email',
                      'product',
                      'policy',
                      'max_device',
                      'creator',
                      'creation_date',
                      'expiration_date',
                      'created',
                      'modified',
                      'snapshot_date']
            bucket = os.environ['GS_SUBSCRIPTIONS_BUCKET']
        elif mode == 'users':
            query = os.environ['QUERY_USERS']
            csvfile = 'users_{}.csv'.format((datetime.datetime.now()).strftime('%Y-%m-%d'))
            schema = ['user_id',
                      'email',
                      'country',
                      'last_active_at',
                      'created',
                      'modified',
                      'snapshot_date']
            bucket = os.environ['GS_USERS_BUCKET']


        # subscriptions_updated
        elif mode == 'subscriptions_updated':
            query = os.environ['QUERY_SUBSCRIPTIONS_UPDATED']
            csvfile = 'subscriptions_updated_{}.csv'.format((datetime.datetime.now()).strftime('%Y-%m-%d'))
            schema = ['subscription_id',
                        'user_id', 
                        'sensopia_id',
                        'assigned_to',
                        'email', 
                        'billing_id', 
                        'workgroup_id', 
                        'product', 
                        'policy', 
                        'max_device', 
                        'creator', 
                        'creation_date', 
                        'expiration_date', 
                        'created', 
                        'modified', 
                        'snapshot_date']
            bucket = os.environ['GS_SUBSCRIPTIONS_UPDATED_BUCKET']



        # users_workgroups
        elif mode == 'users_workgroups':
            query = os.environ['QUERY_USERS_WORKGROUPS']
            csvfile = 'users_workgroups_modified_{}.csv'.format((datetime.datetime.now()).strftime('%Y-%m-%d'))
            schema = ['workgroup_id', 
                        'user_id', 
                        'created', 
                        'modified']
            bucket = os.environ['GS_USERS_WORKGROUPS_BUCKET']


        elif mode == 'api_log_remove':
            query = os.environ['QUERY_API_LOG_REMOVE']
            csvfile = 'api_log_remove_{}.csv'.format((datetime.datetime.now()).strftime('%Y-%m-%d'))
            schema = ['id', 
                        'request', 
                        'response_code',
                        'response', 
                        'created']
            bucket = os.environ['GS_API_LOG_REMOVE_BUCKET']




      
        raw_data = []
        
        try:
            logging.info('is connected? :{}'.format(connection.open))
            cursor = connection.cursor()
            result_rows = cursor.execute(query)
            logging.info('query returned {} rows'.format(result_rows))
            # transform the data
            row = cursor.fetchone()
            while row is not None:
                raw_data.append(row)
                row = cursor.fetchone()

        finally:
            connection.close()
            logging.info('closing connection')

        # upload csv file
        logging.info('Mode: {} - start prep data'.format(mode))

        # data = pd.DataFrame(raw_data, index=schema).transpose()
        data = pd.DataFrame(raw_data, columns=schema)
        data.to_csv(csvfile, index=False) 
        gscloc = upload(csvfile,
                        bucket,
                        format(os.path.basename(csvfile)))
        logging.info("Mode:{} - file uploaded to: {}".format(mode, gscloc))

    except Exception as e:
        status = 'Something went wrong: {}'.format(e)
        logging.exception(status)
        raise e

    return status


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


# upload a csv file to cloud storage
def upload(csvfile, bucketname, blobname):
    client = storage.Client()
    bucket = client.get_bucket(bucketname)
    blob = Blob(blobname, bucket)
    blob.upload_from_filename(csvfile)
    gcslocation = 'gs://{}/{}'.format(bucketname, blobname)
    return gcslocation


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END app]
