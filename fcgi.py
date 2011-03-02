#!/usr/bin/env python
"""
Script for (re)starting django fcgi processes

Usage:
  fcgi.py <project>      # start <project>
  fcgi.py --all          # start all projects

With a project's path as the working directory:
  ../fcgi.py #start the current project

@author: brainrape@chaosmedia.hu
"""


BASE_PATH='/opt/dp'



import os,sys


def start(project):
    workdir = os.path.join(BASE_PATH,project)
    if not os.path.exists(os.path.join(workdir,'manage.py')):
        print 'Error: manage.py not found in '+workdir
        return False

    pidfile = os.path.join(workdir,'pid')
    if os.path.exists(pidfile):
        if os.system('kill `cat -- %s`' % pidfile) != 0:
            print 'Error: Could not kill fcgi process. PID file: %s' % pidfile
            return False
        os.unlink(pidfile)

    command = "/usr/bin/env - " \
        "PYTHONPATH='%(workdir)s' " \
        "PATH='%(workdir)s'" \
        "python %(workdir)s/manage.py runfcgi " \
        "workdir=%(workdir)s " \
        "pidfile=%(workdir)s/pid " \
        "socket=%(workdir)s/socket " \
        "method=threaded " \
        "maxchildren=2 " \
        "outlog=%(workdir)s/out.log errlog=%(workdir)s/err.log"
    if os.system(command % {'workdir':workdir}) !=0:
         print 'Error: error starting fcgi process'
         return False
    if os.system("chmod a+rw %s" % workdir+'/socket') !=0:
         print 'Error: error changing socket permissions'
         return False
    return True

def main():
    # <project>/$ ../fcgi.py     #-> starts project
    if os.getuid() == 0:
        print "Error: it is unsafe to run this script as root"
        return 7
    
    project = None
    if len(sys.argv) == 1:
        if os.path.commonprefix( [os.getcwd(), BASE_PATH] ) == BASE_PATH:
            project = os.getcwd().replace(BASE_PATH,'').strip('/')
    if not project and len(sys.argv)!=2:
        print 'Usage: %s <project_dir>' % sys.argv[0]
        print '    or %s --all' % sys.argv[0]
        sys.exit(1)

    if not project: 
        project = sys.argv[1].strip('/')
    if project == '--all':
        dirs = os.listdir(BASE_PATH)
        projects = []
        for dir in dirs:
            if os.path.isdir(dir) and os.path.exists(os.path.join(dir,'manage.py')):
                projects.append(dir)
        errors=[]
        for project in projects[:]:
            if not start(project):
                errors.append(project)
                projects.remove(project)
        print "started:"," ".join(projects) or 'None'
        if errors:
            print "errors:"," ".join(errors)
    else:
        if start(project):
            print "started",project


if __name__ == "__main__":
    sys.exit(main())

