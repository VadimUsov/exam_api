FROM python:3.12-alpine

WORKDIR /api_pet_store

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["pytest", "-v", "-s", "--alluredir", "allure-results"]
<<<<<<< HEAD
CMD ["tests/test_api_pet_store.py"]
=======
CMD ["tests\test_api_pet_store.py"]
>>>>>>> origin/main
