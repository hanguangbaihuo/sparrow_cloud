#!/bin/bash


docker run sparrow_cloud:unittest /bin/bash -c \
    'source tests/mock_configmap.sh && py.test tests && py.test access_control'