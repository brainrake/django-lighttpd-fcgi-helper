django lighttpd fcgi helpers
============================

This script was written to help host multiple django powered websites
in a lighttpd/fcgi setup.


lighttpd-django.conf.py
-----------------------

include the output of this script in your lighttpd config::

    include_shell /path/to/script/lighttpd-django-conf.py

To deploy a new project, just copy it into BASE_PATH and restart the
web server. Your project should now be running under
http://<project>.<DOMAIN>


fcgi.py
-------

(re)start FCGI processes.

Usage: ::

    fcgi.py <project>      # start <project>
    fcgi.py --all          # start all projects

With a project's path as the working directory: ::

    ../fcgi.py             #start the current project


settings.py
-----------

The only required settings are BASE_PATH and DOMAIN.
Settings can be overridden per project.
