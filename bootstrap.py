#!/usr/bin/env python

"""Google App Engine uses this file to run your Flask application."""

import os
import settings
from utils import adjust_sys_path

adjust_sys_path()
if settings.debug:
    adjust_sys_path('ziplibs')
    # Enable ctypes for Jinja debugging
    # from google.appengine.tools.dev_appserver import HardenedModulesHook
    # HardenedModulesHook._WHITE_LIST_C_MODULES += ['_ctypes', 'gestalt']
else:
    adjust_sys_path(os.path.join('ziplibs.zip', 'ziplibs'))

from app import create_app
from werkzeug_debugger_appengine import get_debugged_app
from flaskext.csrf import csrf
from gae_mini_profiler import profiler, config as profiler_config

profiler_config.enabled_profiler_emails = settings.admin_emails

app = create_app()
csrf(app)
# If we're on the local server, let's enable Flask debugging.
# For more information: http://goo.gl/RNofH
if settings.debug:
    app.debug = True
    app = get_debugged_app(app)
app = profiler.ProfilerWSGIMiddleware(app)
