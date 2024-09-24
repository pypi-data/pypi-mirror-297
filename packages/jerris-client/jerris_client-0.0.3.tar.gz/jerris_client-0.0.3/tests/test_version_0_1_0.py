import datetime
import json
from pathlib import Path

from jerris_jerris_client.const.globals import TYPES_MAPPING
from jerris_jerris_client.const.parameters import PARAMETERS_MAPPING
from jerris_jerris_client.helpers.version_0_0_1 import transform_response_v0_1_0_to_v1_0_0


class TestVersion0_1_0:
    def test_transform_response_v0_1_0_to_v1_0_0(self):
        # Path to the folder containing version 0.1.0 files
        folder_path_v0_1_0 = Path('tests/resources/version_0_1_0')
        folder_path_v1_0_0 = Path('tests/resources/version_1_0_0')

        # Loop over all JSON files in the folder for version 0.1.0
        for json_file_v0_1_0 in folder_path_v0_1_0.glob('*.json'):
            # Load the input data in version 0.1.0 format
            with open(json_file_v0_1_0, 'r') as f:
                response_v0_1_0 = json.load(f)

            # Print the name of the file being processed
            print(f"Processing file: {json_file_v0_1_0.name}")

            # Call the transformation function
            transformed_response = transform_response_v0_1_0_to_v1_0_0(
                response_v0_1_0,
                date_started=datetime.datetime.now(datetime.UTC)
            )

            # Construct the path to the expected file in version 1.0.0
            json_file_v1_0_0 = folder_path_v1_0_0 / json_file_v0_1_0.name

            if json_file_v1_0_0.exists():
                with open(json_file_v1_0_0, 'r') as f:
                    expected_response_v1_0_0 = json.load(f)

                assert transformed_response == expected_response_v1_0_0, \
                    f"Transformed response does not match expected output for {json_file_v0_1_0.name}"
            else:
                assert False, f"Expected file {json_file_v1_0_0.name} not found in version_1_0_0 folder"

            for key in transformed_response['data']:
                parameter_data = transformed_response['data'][key]
                expected_type = PARAMETERS_MAPPING[key]['type']
                real_type = type(parameter_data['result'])

                assert key in PARAMETERS_MAPPING
                assert parameter_data['type'] == expected_type

                if PARAMETERS_MAPPING[key]['multiple']:
                    assert real_type == list, f"Parameter '{key}' should be of type 'list' but real type is '{real_type}' "
                else:
                    assert real_type == TYPES_MAPPING[expected_type], \
                        f"Parameter '{key}' should be of type '{expected_type}' but real type is '{real_type}'"
