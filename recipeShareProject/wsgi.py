"""
WSGI config for recipeShareProject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

#os.path.join(os.path.abspath(os.path.dirname(__file__)), '..')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "recipeShareProject.settings")
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "recipeShareServer_170124_1st_project.settings")

application = get_wsgi_application()
