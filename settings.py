#!/usr/bin/env python
"""
this is the settings file for the lighttpd config generator
"""

BASE_PATH='/opt/dp'
DOMAIN='republicofpoker.com'
ADMIN_MEDIA_PATH="/usr/share/pyshared/django/contrib/admin/media"

EXTRA_CONFIG={
    'my_django_project':{
        'domain':r'^(www\.)?awesomeproject.com$'
    },
    'other_project':{
    }
}
