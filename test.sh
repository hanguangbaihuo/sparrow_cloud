#!/bin/bash


docker run sparrow_cloud:unittest /bin/bash -c \
    'py.test tests && py.test access_control'