import requests
from django.conf import settings

class CallEndpoint:
    def __init__(self, request, domain_key, path_key):
        # Initializer method to set up the object with request, domain, and path keys
        self.request = request  # Store the request object
        self.domain = settings.DOMAIN.get(domain_key)  # Use .get() to avoid KeyError
        self.path = settings.PATH.get(path_key)  # Use .get() to avoid KeyError
        self.url = f"{settings.PROTOCOL}{self.domain}/{self.path}"  # Construct the base URL

    def _headers(self):
        # Method to construct headers for the HTTP request
        return {
            'Authorization': f'Bearer {self.request.headers.get("Authorization")}',  # Get the Authorization header from the request and include it in the headers
            'Content-Type': 'application/json'  # Set the content type to JSON
        }

    def _cookies(self):
        # Method to get cookies from the request
        return self.request.COOKIES  # Return the cookies from the request

    def get_detail(self, entity_id):
        # Method to get details of a specific entity by its ID
        url = f'{self.url}/{entity_id}/'  # Construct the URL for the specific entity
        response = requests.get(
            url,  # URL to send the request to
            headers=self._headers(),  # Include the headers
            cookies=self._cookies()  # Use _cookies() method
        )
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        return response.json()  # Return the response in JSON format

    def get(self, params=None):
        # Method to get a list of entities
        url = f'{self.url}/'  # Construct the URL for the entity list
        response = requests.get(
            url,  # URL to send the request to
            headers=self._headers(),  # Include the headers
            cookies=self._cookies(),  # Use _cookies() method
            params=params
        )
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        return response.json()  # Return the response in JSON format

    def create(self, data):
        # Method to create a new entity
        url = f'{self.url}/'
        response = requests.post(
            url,  # URL to send the request to
            headers=self._headers(),  # Include the headers
            cookies=self._cookies(),  # Use _cookies() method
            json=data  # Send the data as JSON
        )
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        return response.json()  # Return the response in JSON format

    def update(self, entity_id, data):
        # Method to update an existing entity
        url = f'{self.url}/{entity_id}/'  # Construct the URL for the specific entity
        response = requests.put(
            url,  # URL to send the request to
            headers=self._headers(),  # Include the headers
            cookies=self._cookies(),  # Use _cookies() method
            json=data  # Send the data as JSON
        )
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        return response.json()  # Return the response in JSON format

    def delete(self, entity_id):
        # Method to delete a specific entity by its ID
        url = f'{self.url}/{entity_id}/'  # Construct the URL for the specific entity
        response = requests.delete(
            url,  # URL to send the request to
            headers=self._headers(),  # Include the headers
            cookies=self._cookies()  # Use _cookies() method
        )
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        return response.status_code  # Return the HTTP status code