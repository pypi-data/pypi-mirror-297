from datetime import datetime, timedelta
import json
import pytest

from python_everhour.api import EverhourAPI
from python_everhour import config

@pytest.fixture(scope="module")
def vcr_config():
    return {"filter_headers": ["X-Api-Key"]}


@pytest.fixture
def api_key():
    """Fixture to provide a mock API key."""
    return config.everhour.api_key 


@pytest.fixture
def everhour_api(api_key):
    """Fixture to create an EverhourAPI instance with the mock key."""
    return EverhourAPI(api_key)

@pytest.fixture(scope="module")
def vcr():
    return {
        "filter_headers": ["X-Api-Key"],
        "record_mode": "all"  # Change the mode here
    }

@pytest.mark.vcr
def test_check_api_key_connection(everhour_api):
    """Test to check if the API key can successfully connect to the Everhour API."""
    response = everhour_api.get_user()
    response_json = json.loads(response)
    # Check the user id
    assert response_json["id"] == 1304 #https://everhour.docs.apiary.io/#reference/0/users/get-current-user?console=1
    

@pytest.mark.vcr
def test_get_time_entries(everhour_api):
    start_date = datetime.today() - timedelta(days=7)
    end_date = datetime.today()
    response = everhour_api.get_time_entries(start_date, end_date)
    response_json = json.loads(response)
    assert response_json[0]["id"] == 2660155


@pytest.mark.vcr
def test_get_users(everhour_api):
    response = everhour_api.get_users()
    response_json = json.loads(response)
    assert len(response_json) != 0
    assert response_json[0]['role'] == "admin"
