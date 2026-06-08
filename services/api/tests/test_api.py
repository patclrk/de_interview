import pytest
from fastapi.testclient import TestClient

from api.main import app

ALL_CITIES = ["Durham", "Raleigh", "Asheville", "Charlotte"]


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


class TestHealth:
    def test_returns_200(self, client):
        response = client.get("/health")
        assert response.status_code == 200

    def test_returns_ok_status(self, client):
        response = client.get("/health")
        assert response.json() == {"status": "ok"}


class TestTemperatureReadings:
    def test_returns_200(self, client):
        response = client.post("/temperature", json={})
        assert response.status_code == 200

    def test_default_returns_all_cities(self, client):
        response = client.post("/temperature", json={})
        readings = response.json()["readings"]
        assert set(readings.keys()) == set(ALL_CITIES)

    def test_temperature_values_are_numeric(self, client):
        response = client.post("/temperature", json={})
        readings = response.json()["readings"]
        for temp in readings.values():
            assert isinstance(temp, float)

    def test_custom_cities(self, client):
        cities = ["Durham", "Raleigh"]
        response = client.post("/temperature", json={"cities": cities})
        readings = response.json()["readings"]
        assert set(readings.keys()) == set(cities)

    def test_single_city(self, client):
        response = client.post("/temperature", json={"cities": ["Asheville"]})
        readings = response.json()["readings"]
        assert list(readings.keys()) == ["Asheville"]

    def test_unknown_city_is_accepted(self, client):
        response = client.post("/temperature", json={"cities": ["Tokyo"]})
        assert response.status_code == 200
        assert "Tokyo" in response.json()["readings"]

    def test_empty_cities_list_returns_all(self, client):
        response = client.post("/temperature", json={"cities": None})
        readings = response.json()["readings"]
        assert set(readings.keys()) == set(ALL_CITIES)

    def test_response_shape(self, client):
        response = client.post("/temperature", json={})
        body = response.json()
        assert "readings" in body
        assert isinstance(body["readings"], dict)
