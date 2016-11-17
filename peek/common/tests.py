from django.test import TestCase


class MiscTest(TestCase):
    def test_settings(self):
        from peek.settings import common
        from peek.settings import dev
        from peek.settings import prod
