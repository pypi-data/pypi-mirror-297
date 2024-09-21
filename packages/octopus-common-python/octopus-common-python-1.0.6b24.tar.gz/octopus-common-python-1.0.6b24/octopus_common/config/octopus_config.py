import configparser

from octopus_common.constant.Constants import WORKING_DIRECTOR

LOCAL_AUTH_CONFIG = configparser.ConfigParser().read(WORKING_DIRECTOR + '/Auth.properties')
LOCAL_CLIENT_CONFIG = configparser.ConfigParser().read(WORKING_DIRECTOR + '/client.properties')
