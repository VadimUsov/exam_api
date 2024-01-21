import allure
import pytest
from models.pet import Pet
from pydantic import TypeAdapter, ValidationError


class TestGetUsers:
    base_url = "https://petstore.swagger.io/v2"

    @pytest.mark.parametrize("pet, status_code", [
        ({
             "id": 2912,
             "category": {
                 "id": 919,
                 "name": "cosmo_catdog"
             },
             "name": "Nibler_api_test",
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
    @allure.title("Post create a pet.")
    @allure.description("Check that we can create a pet and get right status code in different scenarios.")
    def test_post_create_pet(self, api_pet_store, pet, status_code):
        res = api_pet_store.post_create_pet("/pet", pet)
        with allure.step(f"Check status {res.status_code}"):
            assert res.status_code == status_code
            if status_code == 200:
                data = res.json()
                assert api_pet_store.validate(data, Pet)

    @allure.title("Put update data of a pet. Change its status to sold.")
    @allure.description("Check that we can update a pet if send right status.")
    def test_put_update_pet_sold(self, api_pet_store):
        pet = {
            "id": 2912,
            "category": {
                "id": 919,
                "name": "cosmo_catdog"
            },
            "name": "Nibler_api_test",
            "photoUrls": [
                "string"
            ],
            "tags": [
                {
                    "id": 191,
                    "name": "catdog"
                }
            ],
            "status": "sold"
        }
        res = api_pet_store.put_update_pet("/pet", pet)
        with allure.step(f"Check status {res.status_code}"):
            assert res.status_code == 200
            if res.status_code == 200:
                data = res.json()
                assert api_pet_store.validate(data, Pet)

    @allure.title("Put update data of a pet. Change its status to lost.")
    @allure.description("Check that we cannot update a pet using incorrect status.")
    def test_put_update_pet_lost(self, api_pet_store):
        pet = {
            "id": 2912,
            "category": {
                "id": 919,
                "name": "cosmo_catdog"
            },
            "name": "Nibler_api_test",
            "photoUrls": [
                "string"
            ],
            "tags": [
                {
                    "id": 191,
                    "name": "catdog"
                }
            ],
            "status": "lost"
        }
        res = api_pet_store.put_update_pet("/pet", pet)
        with allure.step(f"Check status {res.status_code}"):
            assert res.status_code == 405

    @allure.title("Put cannot update pet that does not exist.")
    @allure.description("Check that we cannot update a pet that does not exist.")
    def test_put_update_pet_not_exist(self, api_pet_store):
        pet = {
            "name": 123123412312412415,
            "photoUrls": [
                1231234
            ]
        }
        res = api_pet_store.put_update_pet("/pet", pet)
        with allure.step(f"Check status {res.status_code}"):
            assert res.status_code == 404

    @allure.title("Put cannot update a pet using incorrect ID.")
    @allure.description("Check that we cannot update a pet using incorrect ID.")
    def test_put_update_pet_incorrect_id(self, api_pet_store):
        pet = {
            "id": "incorrect id",
            "name": 1231234,
            "photoUrls": [
                1231234
            ]
        }
        res = api_pet_store.put_update_pet("/pet", pet)
        with allure.step(f"Check status {res.status_code}"):
            assert res.status_code == 400

    @allure.title("Get find pets with sold status.")
    @allure.description("Check that we can find a list of pet with sold status.")
    def test_get_find_sold(self, api_pet_store):
        res = api_pet_store.get_find_by_status("/pet/findByStatus", {"status": "sold"})
        with allure.step(f"Check status {res.status_code}"):
            assert res.status_code == 200
        with allure.step(f"Check data of response "):
            data = res.json()
            data_model = TypeAdapter(list[Pet])
            try:
                data_model.validate_python(data)
                assert True
            except ValidationError as e:
                print(e)
                assert False

    @allure.title("Get find pets with lost status.")
    @allure.description("Cannot find pets using wrong status.")
    def test_get_find_lost(self, api_pet_store):
        res = api_pet_store.get_find_by_status("/pet/findByStatus", {"status": "lost"})
        with allure.step(f"Check status {res.status_code}"):
            assert res.status_code == 400

    @pytest.mark.parametrize("pet_id, status_code", [
        ({"petId": 2912}, 200),
        ({"petId": 2912}, 404),
        ({"petId": "one_two"}, 400)
    ])
    @allure.title("Delete pet.{pet_id}")
    @allure.description("Check that we can delete only exists pet with correct ID.")
    def test_get_delete_pet(self, api_pet_store, pet_id, status_code):
        res = api_pet_store.get_find_by_status("/pet/findByStatus", pet_id)
        with allure.step(f"Check status {res.status_code}"):
            assert res.status_code == status_code
