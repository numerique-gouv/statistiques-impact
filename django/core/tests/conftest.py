import pytest
import re
import responses
from rest_framework import status


# METABASE
@pytest.fixture(name="proconnect_MAU")
def fixture_proconnect_monthly_users():
    """Mock Metabase response when fetching ProConnect monthly users."""
    responses.get(
        re.compile(
            r"https://stats.moncomptepro.beta.gouv.fr/public/question/cd934f6d-*"
        ),
        json=[{"Time: Mois": "2025-09-01", "Valeurs distinctes de Sub Fi": "200000"}],
        status=status.HTTP_200_OK,
        content_type="application/json",
    )


@pytest.fixture(name="proconnect_lasuite_MAU")
def fixture_proconnect_lasuite_MAU():
    responses.get(
        re.compile(
            r"https://stats.moncomptepro.beta.gouv.fr/public/question/0e3cee98-*"
        ),
        json=[
            {"Fournisseur Service": "Tchap", "Valeurs distinctes de Sub Fi": 27654},
            {
                "Fournisseur Service": "DINUM - RESANA",
                "Valeurs distinctes de Sub Fi": 23323,
            },
            {"Fournisseur Service": "Grist", "Valeurs distinctes de Sub Fi": 16094},
            {"Fournisseur Service": "Docs", "Valeurs distinctes de Sub Fi": 11515},
            {"Fournisseur Service": "Visio", "Valeurs distinctes de Sub Fi": 8184},
            {"Fournisseur Service": "Fichiers", "Valeurs distinctes de Sub Fi": 1771},
            {
                "Fournisseur Service": "Messagerie de la Suite Numérique",
                "Valeurs distinctes de Sub Fi": 1155,
            },
        ],
        status=status.HTTP_200_OK,
        content_type="application/json",
    )


# DATA GOUV
@pytest.fixture(name="datagouv_messagerie_data")
def fixture_datagouv_messagerie_data():
    responses.get(
        re.compile(r"https://www.data.gouv.fr/*"),
        body="yyyy-mm-dd,utilisateurs uniques la veille, sur les 7 derniers jours, sur les 30 derniers jours\n2025-06-06,369,448,553\n2025-06-07,338,456,558\n2025-06-10,181,422,553\n2025-06-11,390,445,563\n2025-06-12,380,447,558\n2025-06-13,401,445,561\n2025-06-14,378,459,561\n2025-06-15,250,458,558\n2025-06-16,261,458,555\n2025-06-17,404,474,561\n2025-06-18,415,484,574\n2025-06-19,394,483,573\n2025-06-20,403,484,573\n2025-06-21,384,485,576\n2025-06-22,263,485,572\n2025-06-23,266,485,567\n2025-06-24,401,488,573\n2025-06-25,410,478,581\n2025-06-26,407,477,579\n2025-06-27,402,476,575\n2025-06-28,392,474,572\n2025-06-29,270,475,572\n2025-06-30,268,474,572\n2025-07-01,418,482,580\n2025-07-02,428,489,589\n",
        status=status.HTTP_200_OK,
        content_type="application/json",
    )


@pytest.fixture(name="datagouv_file_sent")
def fixture_datagouv_file_sent():
    responses.post(
        re.compile(r"https://demo.data.gouv.fr/api/1/datasets/*"),
        json={
            "checksum": {
                "type": "sha1",
                "value": "47cc980e80adf717d00d8a64c25fcd1395962b56",
            },
            "created_at": "2025-09-04T16:29:00.353226+00:00",
            "description": None,
            "extras": {},
            "filesize": 1545,
            "filetype": "file",
            "format": "csv",
            "harvest": None,
            "id": "d0280651-e268-44de-a7a7-ed515e2bb565",
            "internal": {
                "created_at_internal": "2025-09-04T16:29:00.353226+00:00",
                "last_modified_internal": "2025-09-04T18:29:00.299496+00:00",
            },
            "last_modified": "2025-09-04T18:29:00.299496+00:00",
            "latest": "https://demo.data.gouv.fr/api/1/datasets/r/d0280651-e268-44de-a7a7-ed515e2bb565",
            "metrics": {},
            "mime": "text/csv",
            "preview_url": None,
            "schema": None,
            "success": True,
            "title": "filename",
            "type": "main",
            "url": "https://demo-static.data.gouv.fr/resources/test-envoi-fichiers-france-transfert/20250904-162900/filename",
        },
        status=status.HTTP_201_CREATED,
        content_type="application/json",
    )


@pytest.fixture(name="tchap_MAU")
def fixture_tchap_MAU():
    responses.get(
        re.compile(r"https://stats.tchap.incubateur.net/public/question/ae34205d-*"),
        json=[{"Visit Date": "sept., 2025", "Nombre de lignes": "367 146"}],
        status=status.HTTP_200_OK,
        content_type="application/json",
    )


@pytest.fixture(name="tchap_monthly_messages")
def fixture_tchap_monthly_messages():
    responses.get(
        re.compile(r"https://stats.tchap.incubateur.net/public/question/84a9b0bc-*"),
        json=[
            {"Hour": "août, 2025", "Somme de Events": "5 404 085"},
            {"Hour": "sept., 2025", "Somme de Events": "10 877 632"},
        ],
        status=status.HTTP_200_OK,
        content_type="application/json",
    )


@pytest.fixture(name="posthog_visio_MAU")
def fixture_posthog_visio_MAU():
    responses.get(
        re.compile(r"https://eu.posthog.com*"),
        json={
            "id": 65340,
            "name": "Monthly Active Users",
            "result": [
                {
                    "data": [5728, 3985, 8458, 7533],
                    "days": ["2025-07-01", "2025-08-01", "2025-09-01", "2025-10-01"],
                }
            ],
        },
        status=status.HTTP_200_OK,
        content_type="application/json",
    )
