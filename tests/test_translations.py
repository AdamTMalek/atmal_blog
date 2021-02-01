from django.test import TestCase
from django.test.client import RequestFactory

import atmalblog.translations as translations
from atmalblog.models import Language


class TranslationsTest(TestCase):
    def setUp(self):
        Language.objects.create(code='en', native_name='English')
        Language.objects.create(code='pl', native_name='Polish')
        self.request = RequestFactory().get('/')
        self.request.META = {'HTTP_ACCEPT_LANGUAGE': 'pl,en-GB;q=0.9,en;q=0.8,ru;q=0.7,cs;q=0.6'}

    def test_parse_accepted_languages(self):
        expected = {
            'pl': 1,
            'en': 0.9,
            'ru': 0.7,
            'cs': 0.6,
        }
        actual = translations._parse_accepted_languages(self.request)
        self.assertEquals(expected, actual)

    def test_get_language(self):
        expected = Language.objects.get(code='pl')
        actual = translations._get_language(self.request)
        self.assertEquals(expected, actual)

    def test_translatable(self):
        @translations.translatable
        def translatable_view(request):
            return request.language

        translatable_view_return = translatable_view

        self.assertIsNotNone(translatable_view_return)
