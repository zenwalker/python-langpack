from collections import defaultdict
import warnings
import os

from .exceptions import TranslatorWarning, TranslatorError
from .utils import safe_format, flatten_dict
from .pluralizers import get_plural_form

NOT_RPOVIDED = object()


class BaseTranslator:
    def __init__(self):
        self._translations = defaultdict(dict)
        self._formatters = {}
        self._loaders = {}
        self._hooks = {}

    def set_lang(self, lang):  # pragma: no cover
        raise NotImplementedError()

    def get_lang(self):  # pragma: no cover
        raise NotImplementedError()

    def get_template(self, str_path, values={}, default=None):
        lang = self.get_lang()
        # if str_path in self._hooks[lang]:
        #     str_path = self._hooks[lang][str_path](values)
        return self._translations[lang].get(str_path, default)

    def add_loader(self, loader, extensions):
        assert type(loader) != type, 'Loader should be an instance, not a class.'
        for ext in extensions:
            self._loaders[ext] = loader

    def add_hook(self, lang, str_path, hook_fn):
        self._hooks[lang][str_path] = hook_fn

    def add_formatter(self, formatter, type_names):
        for type_name in type_names:
            if type(type_name) != str:
                type_name = type_name.__name__
            self._formatters[type_name] = formatter

    def add_translations(self, lang, translations):
        self._translations[lang].update(flatten_dict(translations))

    def load_directory(self, directory, recursive=False):
        if recursive:
            tree = os.walk(directory)
            for (dirpath, _, filenames) in tree:
                for filename in filenames:
                    file_path = os.path.join(dirpath, filename)
                    self.load_file(file_path)
        else:
            for file_name in os.listdir(directory):
                file_path = os.path.join(directory, file_name)
                if os.path.isfile(file_path):
                    self.load_file(file_path)

    def load_file(self, file_path):
        ext = os.path.basename(file_path).split('.')[-1]

        try:
            loader = self._loaders[ext]
        except KeyError:
            msg = 'No loader found for {}'.format(file_path)
            warnings.warn(msg, TranslatorWarning)
        else:
            for lang, translations in loader.load_file(file_path).items():
                self.add_translations(lang, translations)

    def translate(self, str_path, **kwargs):
        template = self.get_template(str_path, values=kwargs)
        count = kwargs.get('count', None)

        if not template and count is not None:
            plural_form = get_plural_form(self.get_lang(), count)
            template = self.get_template(str_path + '.' + plural_form)

        if not template:
            return str_path

        return safe_format(template, **kwargs)

    def localize(self, value, format, formatter=None):
        type_name = type(value).__name__
        formatter = self._formatters.get(formatter or type_name)

        if not formatter:
            raise TranslatorError('Formatter for type {} not found'.format(type_name))

        return formatter(value, format, self)


class Translator(BaseTranslator):
    def __init__(self, initial_lang='en', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_lang = initial_lang

    def get_lang(self):
        return self.current_lang

    def set_lang(self, lang):
        self.current_lang = lang
