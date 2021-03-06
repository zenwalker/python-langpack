from django.conf import settings


LANGPACK_LOADERS = getattr(settings, 'LANGPACK_LOADERS', [
    ('langpack.loaders.JsonLoader', ['json']),
])

LANGPACK_FORMATTERS = getattr(settings, 'LANGPACK_FORMATTERS', [
    ('langpack.formatters.format_datetime', ['datetime', 'date', 'time']),
])

LANGPACK_DIRS = getattr(settings, 'LANGPACK_DIRS', settings.LOCALE_PATHS)

LANGPACK_APP_DIRS = getattr(settings, 'LANGPACK_APP_DIR_NAME', ['locale'])

LANGPACK_USE_APP_DIRS = getattr(settings, 'LANGPACK_USE_APP_DIRS', True)

LANGPACK_PLURALIZERS = getattr(settings, 'LANGPACK_PLURALIZERS', {})
