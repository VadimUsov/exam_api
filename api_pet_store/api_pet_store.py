import requests
import allure
from pydantic import BaseModel, ValidationError


class ApiPetStore:

    def __init__(self, base_url: str):
        self._base_url = base_url

    @allure.step("Post create a new pet")
    def post_create_pet(self, path, data) -> requests.Response:
        url = self._base_url + path
        if data is None:
            return requests.post(url)
        else:
            return requests.post(url, json=data)

    @allure.step("Put update pet's data")
    def put_update_pet(self, path, data) -> requests.Response:
        if data is None:
            data = {}
        url = self._base_url + path
        return requests.put(url, json=data)

    @allure.step("Get find pet with status {params}")
    def get_find_by_status(self, path: str, params=None) -> requests.Response:
        if params is None:
            params = []
        url = self._base_url + path
        return requests.get(url, params)

    @allure.step("Delete pet with ID {params}")
    def delete_pet(self, path: str, params=None) -> requests.Response:
        if params is None:
            params = []
        url = self._base_url + path
        return requests.delete(url, params)

    @allure.step("Validate response data")
    def validate(self, result: object, model: BaseModel) -> bool:
        try:
            model.model_validate(result, strict=True)
            return True
        except ValidationError as e:
            print(e)
            return False
