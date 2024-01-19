import pytest
from api_pet_store.api_pet_store import ApiPetStore


@pytest.fixture(scope="class")
def api_pet_store(request):
    base_url = getattr(request.cls, "base_url")
    return ApiPetStore(base_url)


