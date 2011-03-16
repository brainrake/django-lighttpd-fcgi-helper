#!/usr/bin/env python
"""
Output lighttpd configuration files for django projects in BASE_PATH.

Any subdirectory of BASE_PATH which contains 'manage.py' is considered a project.

Projects will be served from http://<project>.DOMAIN by default

FCGI processes must be started separately with fcgi.py.
"""

try: from settings import *
except: pass


TEMPLATE='''
$HTTP["host"] =~ "%(domain)s" {
  fastcgi.server = (
    "/fcgi" => (
        "main" => (
            "socket" => "%(socket)s",
            "check-local" => "disable",
            "fix-root-scriptname" => "enable",
        )
    ),
  )

  url.rewrite-once = (
    "^(/media.*)$" => "$1",
    "^(/admin_media.*)$" => "$1",
    "^/favicon\.ico$" => "/media/favicon.ico",
    "^(/.*)$" => "/fcgi$1",
  )
  alias.url = (
    "/admin_media" => "%(ADMIN_MEDIA_PATH)s",
    "/media" => "%(BASE_PATH)s/%(project)s/media",
  )
}

'''


import os

projects=[]
os.chdir(BASE_PATH)
dirs = os.listdir(BASE_PATH)
dirs.sort()
for dir in dirs:
    if os.path.isdir(dir) and os.path.exists(os.path.join(dir,'manage.py')):
            projects.append(dir)

for project in projects:
    try: conf = EXTRA_CONFIG[project]
    except KeyError: conf={}
    print TEMPLATE % {
        'BASE_PATH':BASE_PATH,
        'ADMIN_MEDIA_PATH':ADMIN_MEDIA_PATH,
        'domain': conf.get('domain',r"^%s.%s$" % (project,DOMAIN)),
        'project':project,
        'socket':os.path.join(BASE_PATH, project, 'socket'),
    }

