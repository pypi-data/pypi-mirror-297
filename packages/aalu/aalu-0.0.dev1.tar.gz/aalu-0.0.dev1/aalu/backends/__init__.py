"""
Provides the default backend
"""

from aalu.backends.file import TEMP_FILE_BACKEND
from aalu.backends.rest import AALU_REST_BACKEND
from aalu.backends.zipkin import AALU_ZIPKIN_BACKEND

DEFAULT_BACKEND = AALU_ZIPKIN_BACKEND or AALU_REST_BACKEND or TEMP_FILE_BACKEND
