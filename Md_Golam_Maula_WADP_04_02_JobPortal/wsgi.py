"""
WSGI config for Md_Golam_Maula_WADP_04_02_JobPortal project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Md_Golam_Maula_WADP_04_02_JobPortal.settings')

application = get_wsgi_application()
