import pytest
from django.test.client import Client
from django_plugin_django_header.middleware import COMPOSITIONS, remove_diacritics


@pytest.mark.django_db
def test_django_header():
    response = Client().get("/admin/")
    expected = [remove_diacritics(composition) for composition in COMPOSITIONS]
    assert response["Django-Composition"] in expected
