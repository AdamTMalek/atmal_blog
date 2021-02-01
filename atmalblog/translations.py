import re
from typing import Dict

from .models import Language


def translatable(func):
    """
    This decorator is meant to be used on a view.

    It adds a language property to the request with a reference to the language
    that has been negotiated through the use of the ACCEPT-LANGUAGE request
    headings by the client, and the languages supported (models in the database).

    :param func: View function with a request as a parameter,
    """

    def fetch_language(request, *args, **kwargs):
        request.language = _get_language(request)
        return func(request, *args, **kwargs)

    return fetch_language


def _get_language(request) -> Language:
    """
    Performs language negotiation and returns the negotiated language
    :param request: Django's request (as passed to a view function)
    :return: Language object that represents the negotiated language.
    """
    accepted_languages = _parse_accepted_languages(request)
    supported_languages = Language.objects.all()
    for language in accepted_languages.keys():
        if len(supported_languages.filter(code=language)) > 0:  # Use filter, as get throws an exception
            return supported_languages.get(code=language)  # Get the language

    return Language.objects.get(code='en')  # Use the default language - English


def _parse_accepted_languages(request) -> Dict[str, int]:
    """
    Parses the ACCEPT-LANGUAGE list present in the request
    with optional weights and returns a dictionary
    of accepted languages by the client
    :param request: Django's request (as passed to a view function)
    :return: Dictionary of accepted languages. Key is the language code, value is its weight.
    """
    accepted_languages = {}
    languages_regex = re.compile(r'([\w\-\d.=;]+)')  # Takes language code with the optional weight
    matches = languages_regex.findall(request.META.get('HTTP_ACCEPT_LANGUAGE'))
    for match in matches:
        language = match[:2]  # Take the language code
        weight = 1 if (w := match.partition('=')) else w  # If the weight is present - use it, otherwise set to 1
        accepted_languages[language] = weight

    return accepted_languages
