from __future__ import absolute_import, unicode_literals
import pkg_resources
from .celery_apps import app as celery_app
try:
    __version__ = pkg_resources.get_distribution("garden_monitor").version
except:
    __version__ = "dev"
__all__ = ('celery_app', "__version__")
