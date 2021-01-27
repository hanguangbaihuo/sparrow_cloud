import os
import json
import logging

from django.conf import settings

from sparrow_cloud.utils.get_settings_value import get_settings_value
from sparrow_cloud.restclient import rest_client

logger = logging.getLogger(__name__)

def add_lock():
    """
        # ConfigMap:
            SC_SPARROW_DISTRIBUTED_LOCK_SVC
            SC_SPARROW_DISTRIBUTED_LOCK_API
    """
    pass

def remove_lock():
    pass
