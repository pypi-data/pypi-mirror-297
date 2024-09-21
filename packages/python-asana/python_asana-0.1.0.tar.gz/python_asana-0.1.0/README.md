# AsanaAPI Library 
This library provides a simple interface to interact with the Asana [API](https://developers.asana.com/docs/api-features).

## Tests Overview
We have implemented unit tests to validate the behavior of the Asana API query functionality using mocked requests and responses. These tests simulate API interactions by patching the requests.get method and using custom mock responses (using the `unittest.mock.patch`). This allows us to test various scenarios without needing actual API calls, ensuring that our application behaves as expected.