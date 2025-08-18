"""
Tests for the generated openapi schema.
"""

import json
from io import StringIO

from django.core.management import call_command
from django.test import Client

import pytest

pytestmark = pytest.mark.django_db


def test_openapi_client_schema():
    """
    Generated and served OpenAPI client schema should be correct.
    The spectacular command reloads test env.
    """
    # Start by generating the swagger.json file
    output = StringIO()
    call_command(
        "spectacular",
        "--urlconf",
        "core.api_urls",
        "--format",
        "openapi-json",
        "--file",
        "core/tests/swagger.json",
        stdout=output,
    )
    assert output.getvalue() == ""

    response = Client().get("/api/swagger.json")

    assert response.status_code == 200
    with open("core/tests/swagger.json", "r", encoding="utf-8") as expected_schema:
        assert response.json() == json.load(expected_schema)
