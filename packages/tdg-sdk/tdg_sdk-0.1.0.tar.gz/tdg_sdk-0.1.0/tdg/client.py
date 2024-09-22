import requests

class TDGClient:
    def __init__(self, base_url="http://98.82.50.63:8000", token=None):
        """
        Initialize the TDGClient.
        :param base_url: str, The base URL of the API
        :param token: str, Bearer token for authentication (optional)
        """
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.headers = {
            'Content-Type': 'application/json',
        }
        if self.token:
            self.headers['Authorization'] = f'Bearer {self.token}'

    def _get(self, endpoint, params=None):
        """
        Helper method to make GET requests.
        :param endpoint: str, API endpoint
        :param params: dict, Query parameters (optional)
        :return: dict, JSON response
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    def _post(self, endpoint, data=None, files=None):
        """
        Helper method to make POST requests.
        :param endpoint: str, API endpoint
        :param data: dict, Data to be sent in the POST request
        :param files: dict, Files to be uploaded in the POST request
        :return: dict, JSON response
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        # Adjust headers for file upload if files are present
        headers = self.headers.copy()
        if files:
            headers.pop('Content-Type')  # Let requests library set the Content-Type for multipart/form-data

        response = requests.post(url, headers=headers, json=data if not files else None, files=files)
        response.raise_for_status()
        return response.json()

    def login(self, email, password):
        """
        Login and authenticate the user.
        :param email: str
        :param password: str
        :return: dict, JSON response with user info and tokens
        """
        data = {
            'email': email,
            'password': password
        }
        response = self._post('/api/v1/auth/login/', data)
        
        # Extract access and refresh tokens from the response data
        if response.get('status') and response.get('data'):
            self.access_token = response['data'].get('access')
            self.refresh_token = response['data'].get('refresh')
            
            # Set Authorization header with the access token
            if self.access_token:
                self.headers['Authorization'] = f'Bearer {self.access_token}'
        
        return response

    def register(self, email, password, cpassword):
        """
        Register a new user.
        :param email: str
        :param password: str
        :param cpassword: str, Confirm password
        :return: dict, JSON response with registration status
        """
        data = {
            'email': email,
            'password': password,
            'cpassword': cpassword  # Confirm password field
        }
        return self._post('/api/v1/auth/register/', data)

    def upload_file(self, file_path, additional_data=None):
        """
        Upload a file.
        :param file_path: str, Path to the file to be uploaded
        :param additional_data: dict, Additional data to send with the file (optional)
        :return: dict, JSON response from the server
        """
        files = {'file': open(file_path, 'rb')}
        data = additional_data if additional_data else {}
        return self._post('/api/v1/upload/', data=data, files=files)

    def set_base_url(self, new_base_url):
        """
        Dynamically update the base URL for future requests.
        :param new_base_url: str, The new base URL
        """
        self.base_url = new_base_url.rstrip("/")
