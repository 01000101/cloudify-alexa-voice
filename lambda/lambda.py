'''
    Alexa Skills application for Gigaspaces Cloudify manager
'''
# Logging
import logging
# Requests
from requests.exceptions import ConnectionError
# Cloudify API
from cloudify_rest_client import CloudifyClient
from cloudify_rest_client.exceptions import CloudifyClientError


# Set up the logger
LOG = logging.getLogger()
LOG.setLevel(logging.DEBUG)
# Set up valid application IDs
VALID_APP_IDS = [
    'amzn1.ask.skill.[unique-value-here]'
]
# Cloudify endpoint
CFY_ENDPOINT = '[manager-ip-here]'


def validate_session(session):
    '''Validates a device by session information'''
    app = session.get('application')
    if not app or 'applicationId' not in app:
        LOG.error('Missing application ID in request')
        return False
    if app['applicationId'] not in VALID_APP_IDS:
        LOG.error('The application ID (%s) is not allowed',
                  app['applicationId'])
        return False
    return True


def cloudify_is_running(client):
    '''Checks if a Cloudify Manager is running'''
    LOG.debug('Fetching Cloudify status')
    try:
        return client.manager.get_status().get('status') == 'running'
    except (ConnectionError, CloudifyClientError, ValueError) as exc:
        LOG.error('Exception: %s', str(exc))
        return None


def get_cloudify_version(client):
    '''Get the version of a Cloudify manager'''
    LOG.debug('Fetching Cloudify version')
    try:
        return client.manager.get_version().get('version')
    except (ConnectionError, CloudifyClientError, ValueError) as exc:
        LOG.error('Exception: %s', str(exc))
        return None


def get_cloudify_blueprints(client):
    '''Gets a list of all Cloudify manager blueprints'''
    LOG.debug('Fetching Cloudify blueprints')
    try:
        return client.blueprints.list() or list()
    except (ConnectionError, CloudifyClientError) as exc:
        LOG.error('Exception: %s', str(exc))
        return list()


def get_cloudify_executions(client):
    '''Gets a list of all Cloudify manager executions'''
    LOG.debug('Fetching Cloudify executions')
    try:
        return client.executions.list() or list()
    except (ConnectionError, CloudifyClientError) as exc:
        LOG.error('Exception: %s', str(exc))
        return list()


def lambda_handler(event, context):
    '''Function entry point'''
    content = None
    LOG.info('entry(): %s', event)
    # Validate application / device
    LOG.debug('Validating application')
    if not validate_session(event.get('session', dict())):
        return {}
    LOG.debug('Application is valid')
    # Get Cloudify client
    client = CloudifyClient(CFY_ENDPOINT)
    try:
        client.manager.get_status()
    except ConnectionError:
        return build_response(
            {}, 'Sorry, the Cloudify manager appears to be offline')
    # Handle types
    request = event['request']
    if request['type'] == 'IntentRequest':
        if request['intent']['name'] == 'GetCloudifyStatusIntent':
            content = 'The Cloudify manager is %s' % (
                'running' if cloudify_is_running(client) else 'not running')
        elif request['intent']['name'] == 'GetCloudifyVersionIntent':
            version = get_cloudify_version(client)
            content = 'Sorry, I could not get the Cloudify manager version' \
                      if not version else \
                      'The Cloudify manager is at version %s' % version
        elif request['intent']['name'] == 'GetCloudifyBlueprintsCountIntent':
            blueprints = get_cloudify_blueprints(client)
            content = 'There are no blueprints installed' \
                      if not blueprints else \
                      'There are %d blueprints installed' % len(blueprints)
        elif request['intent']['name'] == 'GetCloudifyExecutionsCountIntent':
            executions = [x for x in get_cloudify_executions(client)
                          if x['status'] == 'running']
            content = 'There are no executions running' \
                      if not executions else \
                      'There %s %d executions running' % (
                          'is' if len(executions) == 1 else 'are',
                          len(executions)
                      )
    # Handle unknown issues or Lambda tests
    if not content:
        content = 'Sorry, I did not understand the request'
    # Return
    return build_response({}, content)


def build_response(session, content):
    '''Builds a response for Alexa'''
    return {
        "version": "1.0",
        "sessionAttributes": session,
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": content
            }
        }
    }
