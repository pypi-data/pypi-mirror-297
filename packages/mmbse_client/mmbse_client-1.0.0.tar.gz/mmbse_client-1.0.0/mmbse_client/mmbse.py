import logging
from dataclasses import dataclass
from typing import Dict, List, Optional, Union

import requests
from requests import Response


@dataclass
class MMBSE_Model:
    model_id: int
    name: str
    artefacts: List[str]
    queries: Dict[str, type]
    output_parameters: Dict[str, str]
    input_parameters: Dict[str, str]
    input_artefacts: List[str]
    input_dependencies: Dict[str, "MMBSE_Model"]


class APIClient:
    """A generic Rest API wrapper"""

    def __init__(self, base_url: str, api_token: str) -> None:
        """Create a new API wrapper

        :param base_url: The base URL for the API
        """
        self._base_url = base_url
        self.headers = {"Authorization": f"Token {api_token}"}

    def get(self, endpoint: str, params: dict = None) -> requests.Response:
        """Send a GET request to the API.
        GET requests are used for retrieving data from the API.

        :param endpoint: The API endpoint
        :param params: The query parameters
        :return: The response from the API
        """
        response = requests.get(
            f"{self._base_url}/{endpoint}", headers=self.headers, params=params
        )

        if response.status_code == 200:
            return response
        else:
            raise Exception(f"Server returned status code {response.status_code}")

    def post(self, endpoint: str, data: dict = None, files=None) -> requests.Response:
        """Send a POST request to the API.
        POST requests are used for creating new data.

        :param endpoint: The API endpoint
        :param data: The data to send in the request body
        :return: The response from the API
        """
        response = requests.post(
            f"{self._base_url}/{endpoint}", headers=self.headers, json=data, files=files
        )

        if response.status_code == 201:
            return response
        print(response.text)
        raise Exception(f"Server returned status code {response.status_code}")

    def post_file(
        self, endpoint: str, data: dict = None, files=None
    ) -> requests.Response:
        """Send a POST request to the API.
        POST requests are used for creating new data.

        :param endpoint: The API endpoint
        :param data: The data to send in the request body
        :return: The response from the API
        """
        response = requests.post(
            f"{self._base_url}/{endpoint}", headers=self.headers, data=data, files=files
        )

        if response.status_code == 201:
            return response
        print(response.text)
        raise Exception(f"Server returned status code {response.status_code}")

    def put(self, endpoint: str, data: dict = None) -> requests.Response:
        """Send a PUT request to the API.
        PUT requests are used for updating existing data.

        :param endpoint: The API endpoint
        :param data: The data to send in the request body
        :return: The response from the API
        """
        return requests.put(
            f"{self._base_url}/{endpoint}", headers=self.headers, json=data
        )

    def delete(self, endpoint: str) -> requests.Response:
        """Send a DELETE request to the API.
        DELETE requests are used for deleting existing data.

        :param endpoint: The API endpoint
        :return: The response from the API
        """
        response = requests.delete(f"{self._base_url}/{endpoint}", headers=self.headers)

        if response.status_code != 204:
            raise Exception(f"Server returned status code {response.status_code}")
        else:
            return response


class MMBSE(APIClient):
    """A wrapper for the MMBSE REST API"""

    def __init__(self, api_token: str, base_url: str = "https://mmbse.app.cern.ch/api"):
        """Create a new MMBSE API wrapper
        param api_token: The API token for the MMBSE API
        param base_url: The base URL for the MMBSE API (defaults to the production API)

        """
        super().__init__(base_url, api_token)

    def get_systems(self) -> Dict[str, str]:
        """Retrieve a dictionary of systems from the API

        :return: A dictionary containing all systems in the database
        """
        return self.get("systems").json()

    def get_system(self, system: Union[str, int]) -> Dict[str, str]:
        """Retrieve a specific system from the API

        :param system: The name or ID of the system
        :return: A dictionary containing the system information
        """
        return self.get(f"systems/{system}").json()

    def get_system_models(self, system: Union[str, int]) -> List[str]:
        """Retrieve a list of models for a specific system from the API

        :param system: The name or ID of the system
        :return: A list of model names
        """
        return self.get(f"systems/{system}/models").json()

    def get_system_model(
        self, system: Union[str, int], model_name: str
    ) -> Dict[str, str]:
        """Retrieve a specific system model from the API

        :param system: The name or ID of the system
        :param model_name: The name of the model
        :return: A dictionary containing the model information
        """
        return self.get(f"systems/{system}/models/{model_name}").json()

    def create_system(
        self,
        name: str,
        type: str,
        description: str = "",
        tags: List[str] = None,
        image_1=None,
        image_2=None,
        image_3=None,
        owner: str = "",
        official_system_references: List[str] = None,
    ) -> Dict[str, str]:
        """
        Create a new system in the MMBSE API.

        This method sends a POST request to the MMBSE API to create a new system
        with the provided details.

        :param name: The name of the system. This is a required parameter.
        :param type: The type of the system. This is a required parameter.
        :param description: A brief description of the system. This is an optional
        parameter with a default value of an empty string.
        :param tags: A list of tags associated with the system. This is an optional
        parameter with a default value of None.
        :param image_1: The URL of the first image associated with the system. This
        is an optional parameter with a default value of None.
        :param image_2: The URL of the second image associated with the system. This
        is an optional parameter with a default value of None.
        :param image_3: The URL of the third image associated with the system. This
        is an optional parameter with a default value of None.
        :param owner: The owner of the system. This is an optional parameter with a
        default value of an empty string.
        :param official_system_references: A list of official system references. This
        is an optional parameter with a default value of None.
        :return: A dictionary containing the response from the API. The dictionary
        includes details of the created system.
        """
        if tags is None:
            tags = []
        if official_system_references is None:
            official_system_references = []
        system_data = {
            "type": type,
            "name": name,
            "description": description,
            "image_1": image_1,
            "image_2": image_2,
            "image_3": image_3,
            "owner": owner,
        }

        if tags:
            system_data["tags"] = tags
        if official_system_references:
            system_data["official_system_references"] = official_system_references

        return self.post("systems/", system_data).json()

    def delete_system(self, system: str) -> None:
        """Delete a system

        :param system: The name or ID of the system
        """
        self.delete(f"systems/{system}")
        logging.info(f"Successfully deleted system: {system}")

    def get_model(self, model: str) -> Dict[str, str]:
        """Retrieve a specific model from the API

        :param model: The name or ID of the model
        :return: A dictionary containing the model information
        """
        return self.get(f"models/{model}").json()

    def create_model(
        self,
        system: str,
        name: str,
        description: str,
        type: str,
        design_step: str,
        comment: str = "",
        inputs=None,
        outputs=None,
    ) -> MMBSE_Model:
        """Create a new model in the MMBSE API and associate it with a system."""
        if inputs is None:
            inputs = []
        if outputs is None:
            outputs = []

        model_data = {
            "name": name,
            "description": description,
            "system": system,
            "type": type,
            "design_step": design_step,
            "comment": comment,
            "inputs": inputs,
            "outputs": outputs,
        }

        return self.post("models/", model_data).json()

    def delete_model(self, model: str) -> None:
        """Delete a model

        :param system: The name or ID of the system
        """
        self.delete(f"models/{model}")
        logging.info(f"Successfully deleted system: {model}")

    def get_model_output_parameter_value(
        self, model: str, parameter_name: str
    ) -> Response:
        """Retrieve the value of an output parameter for a specific model from the API

        :param model: The name or ID of the model
        :param parameter_name: The name of the output parameter
        :return: The value of the output parameter
        """
        return self.get(
            f"models/{model}/get_output_parameter_value/{parameter_name}"
        ).json()

    def get_model_output_parameter_list(self, model: str) -> Response:
        """Retrieve a list of output parameters for a specific model from the API

        :param model: The name or ID of the model
        :return: A list of output parameters
        """
        return self.get(f"models/{model}/get_output_parameter_list").json()

    def create_model_output_parameter(
        self, model: str, name: str, value: str
    ) -> Response:
        """Create a new output parameter for a specific model in the MMBSE API

        :param model: The name or ID of the model
        :param name: The name of the output parameter
        :param value: The value of the output parameter
        :return: The response from the API
        """
        parameter_data = {"model": model, "name": name, "value": value}
        return self.post(f"models/{model}/add_output_parameter/", parameter_data).json()

    def get_model_input_file_list(self, model: str) -> Response:
        """Retrieve a list of input files for a specific model from the API

        :param model: The name or ID of the model
        :return: A list of input files
        """
        return self.get(f"models/{model}/inputs").json()

    def get_model_output_file_list(self, model: str) -> Response:
        """Retrieve a list of output files for a specific model from the API

        :param model: The name or ID of the model
        :return: A list of output files
        """
        return self.get(f"models/{model}/outputs").json()

    def download_model_input_files(self, model: str) -> list[int]:
        """Download input files for a specific model from the API

        :param model: The name or ID of the model
        """
        name_list = []
        files = self.get_model_input_file_list(model)
        for file in files:
            name_list.append(file["name"])
            self.download_file(file["name"], file["file"])

        return name_list

    def get_model_roxie_data_filename(self, model: str) -> Optional[str]:
        files = self.get_model_input_file_list(model)
        return next(
            (file["name"] for file in files if file["name"].endswith(".data")),
            None,
        )

    def upload_model_input_file(
        self, model: str, name: str, file_path: str
    ) -> Response:
        """Upload an input file for a specific model to the API

        :param model: The name or ID of the model
        :param name: The name of the file
        :param file_path: The path of the file to upload
        :return: The response from the API
        """
        data = {
            "name": name,
            "type": "FILE",
        }
        file = {"file": open(file_path, "rb")}
        print(file)
        return self.post_file(f"models/{model}/inputs", data=data, files=file)

    def upload_model_output_file(
        self, model: str, name: str, file_path: str
    ) -> Response:
        """Upload an output file for a specific model to the API

        :param model: The name or ID of the model
        :param name: The name of the file
        :param file_path: The path of the file to upload
        :return: The response from the API
        """
        data = {
            "name": name,
            "type": "FILE",
        }
        file = {"file": open(file_path, "rb")}
        return self.post_file(f"models/{model}/outputs", data=data, files=file)

    def upload_model_file(
        self, mode: str, model: str, name: str, file_path: str
    ) -> Response:
        """Upload an output file for a specific model to the API

        :param mode: The mode of the file (input or output)
        :param model: The name or ID of the model
        :param name: The name of the file
        :param file_path: The path of the file to upload
        :return: The response from the API
        """
        data = {
            "name": name,
            "type": "FILE",
        }
        file = {"file": open(file_path, "rb")}
        if mode == "input":
            return self.post_file(f"models/{model}/inputs", data=data, files=file)
        elif mode == "output":
            return self.post_file(f"models/{model}/outputs", data=data, files=file)
        else:
            raise Exception(f"Invalid mode {mode}")

    @staticmethod
    def download_file(name: str, url: str) -> None:
        """Download an input file from the API

        :param name: The name of the file
        :param url: The URL of the file
        :return: The file contents
        """
        response = requests.get(url).content
        with open(name, "wb") as file:
            file.write(response)

    def get_user_details(self) -> Response:
        """Retrieve details of the currently authenticated user from the API

        :return: The response from the API
        """
        return self.get("user-details").json()

    def is_authenticated(self) -> bool:
        """Check if the user is logged in

        :return: True if the user is logged in, False otherwise
        """
        try:
            self.get_user_details()
            return True
        except Exception:
            return False

    def load_model(self, system, modelname) -> MMBSE_Model:
        pass

    def load_artefact(self, model, artefact, iteration="latest"):
        pass

    def load_query(self, model, query, iteration="latest"):
        pass

    def add_visual(self, model):
        pass

    def add_iteration(
        self,
        model,
        execution_type,
        file,
        description,
        output_files,
        output_params,
        visuals,
        auto_report,
        report_alternive,
    ):
        pass

    def iteration_add_values(
        self,
        model_iteration,
        output_files,
        output_params,
        visuals,
        auto_report,
        report_alternive,
    ):
        pass

    def add_query(self, model, query_name, return_type, func):
        pass

    def check_cache(self, model):
        pass

    def get_cached_results(self):
        pass


def as_file(data: str):
    """Return string data as a file accessible by target"""
