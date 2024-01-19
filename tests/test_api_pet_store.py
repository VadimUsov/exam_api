import allure
from models.pet import Pet
import pytest


class TestGetUsers:
    base_url = "https://petstore.swagger.io/v2"

    pet = {
        "id": 2912,
        "category": {
            "id": 919,
            "name": "cosmo_catdog"
        },
        "name": "Nibler",
        "photoUrls": [
            "string"
        ],
        "tags": [
            {
                "id": 191,
                "name": "catdog"
            }
        ],
        "status": "available"
    }

    @pytest.mark.parametrize("pet, status_code", [
        ({
            "id": 2912,
            "category": {
                "id": 919,
                "name": "cosmo_catdog"
            },
            "name": "Nibler",
            "photoUrls": [
                "string"
            ],
            "tags": [
                {
                    "id": 191,
                    "name": "catdog"
                }
            ],
            "status": "available"
        }, 200),
        ({}, 405),
        (None, 415)
    ])
    @allure.title("")
    @allure.description("")
    def test_post_create_pet(self, api_pet_store, pet, status_code):
        res = api_pet_store.post_create_pet("/pet", pet)
        print(res.content)
        with allure.step(f"Check status "):
            assert res.status_code == status_code
            if status_code == 200:
                data = res.json()
                assert api_pet_store.validate(data, Pet)
