from typing import Any, Dict, List, Optional
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

class APIResponseRenderer(JSONRenderer):
    """
    Renderer used to modify the structure of response to include custom
    parameters like `message` and `successful`.

    The APIView class using this renderer should specify the `response_format`
    dictionary to make use of this renderer.

    Keys that can be present in the `response_format` dictionary:
        1. success_message: str.
        2. error_message: str | None.
        3. success_data_key: str | None.
        4. error_data_key: str | None.
        5. Any other items present in the dictionary would be picked up as it
           is and will be added to the response.

    By default, the original data is stored in response dictionary using `data` as key.
    You can overide this behaviour by providing `success_data_key` and / or
    `error_data_key` value in `response_format`.

    Note: If `response_format` dictionary is not provided to the APIView class,
    this renderer will work like `JSONRenderer`.
    """

    settings_key = "response_format"
    success_message_key = "success_message"
    error_message_key = "error_message"
    success_data_key = "success_data_key"
    error_data_key = "error_data_key"
    default_data_key = "data"

    def render(self, data, accepted_media_type = None, renderer_context = None):
        if renderer_context is None:
            return super().render(data, accepted_media_type, renderer_context)

        if not hasattr(renderer_context["view"], self.settings_key):
            return super().render(data, accepted_media_type, renderer_context)

        response_format: Dict[str, Any] = getattr(renderer_context["view"], self.settings_key)

        is_successful = self.is_successful_request(renderer_context["response"])
        data_key_string = self.success_data_key if is_successful else self.error_data_key
        data_key = response_format.get(data_key_string, self.default_data_key)

        final_data = {}
        final_data["success"] = is_successful

        # fill message field
        if is_successful:
            # TODO: Check types using isInstance
            final_data["message"] = response_format.get(self.success_message_key, "")
        else:
            # TODO: Check types using isInstance
            final_data["message"] = response_format.get(self.error_message_key, "")

        config_keys = self.get_config_keys()

        # Add rest of the additional data supplied
        for key, value in response_format.items():
            if key in config_keys:
                continue
            # TODO: Check types using isInstance
            final_data[key] = value

        # Finally adding the original data in the `data_key`
        final_data[data_key] = data

        return super().render(final_data, accepted_media_type, renderer_context)


    def is_successful_request(self, response: Optional[Response]) -> bool:
        if response is None:
            return False

        return response.status_code >= 200 and response.status_code < 300


    def get_config_keys(self) -> List[str]:
        return [
            self.success_message_key,
            self.error_message_key,
            self.success_data_key,
            self.error_data_key,
        ]
