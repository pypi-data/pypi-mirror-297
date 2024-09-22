# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import base64
import json
import os
import subprocess
from uuid import uuid4


def dict_to_b64_string(dict_to_encode: dict) -> str:
    """Encode a dictionary to a base64-encoded string.

    Args:
        dict_to_encode: The dictionary to encode.

    Returns:
        The base64-encoded string.
    """
    json_string = json.dumps(dict_to_encode)
    return base64.b64encode(json_string.encode("utf-8")).decode("utf-8")


def count_lines_in_file(file_path):
    """Count the number of lines in a file.

    Args:
        file_path: The path to the file.

    Returns:
        The number of lines in the file.
    """
    wc = subprocess.check_output(["wc", "-l", file_path])
    return int(wc.decode("utf-8").split()[0])


def get_input_files(pipe_result: str, input_files: list) -> list:
    """Set the input files for the task.

    Args:
        pipe_result: The result of the previous task (from Celery).
        input_files: The input files for the task.

    Returns:
        The input files for the task.
    """
    if pipe_result:
        result_string = base64.b64decode(pipe_result.encode("utf-8")).decode("utf-8")
        result_dict = json.loads(result_string)
        input_files = result_dict.get("output_files")
    return input_files


def task_result(
    output_files: list, workflow_id: str, command: str, meta: dict = None
) -> str:
    """Create a task result dictionary and encode it to a base64 string.

    Args:
        output_files: List of output file dictionaries.
        workflow_id: ID of the workflow.
        command: The command used to execute the task.
        meta: Additional metadata for the task (optional).

    Returns:
        Base64-encoded string representing the task result.
    """
    result = {
        "output_files": output_files,
        "workflow_id": workflow_id,
        "command": command,
        "meta": meta,
    }
    return dict_to_b64_string(result)


class OutputFile:
    """Represents an output file.

    Attributes:
        uuid: Unique identifier for the file.
        display_name: Display name for the file.
        filename: Filename for the file.
        path: Full path to the file.
    """

    def __init__(
        self,
        output_path: str,
        filename: str = None,
        file_extension: str = None,
        data_type: str = None,
    ):
        """Initialize an OutputFile object.

        Args:
            output_path: The path to the output directory.
            filename: The name of the output file (optional).
            file_extension: The extension of the output file (optional).
        """
        self.uuid = uuid4().hex
        self.display_name = self._generate_display_name(filename, file_extension)
        self.data_type = data_type
        self.filename = self._generate_filename(file_extension)
        self.path = os.path.join(output_path, self.filename)

    def _generate_filename(self, file_extension: str = None):
        """Generate the filename for the output file based on the UUID.

        Args:
            file_extension: The extension of the output file (optional).

        Returns:
            The filename for the output file.
        """
        return f"{self.uuid}.{file_extension}" if file_extension else self.uuid

    def _generate_display_name(
        self, filename: str = None, file_extension: str = None
    ) -> str:
        """Generate the display name for the output file.

        Args:
            filename: The name of the input file (optional).
            file_extension: The extension of the output file (optional).

        Returns:
            The display name for the output file.
        """
        base_name = filename if filename else self.uuid
        return f"{base_name}.{file_extension}" if file_extension else base_name

    def to_dict(self):
        """Return a dictionary representation of the OutputFile object.

        Returns:
            A dictionary containing the attributes of the OutputFile object.
        """
        return {
            "filename": self.filename,
            "display_name": self.display_name,
            "data_type": self.data_type,
            "uuid": self.uuid,
            "path": self.path,
        }


def create_output_file(
    output_path: str,
    filename: str = None,
    file_extension: str = None,
    data_type: str = "worker:generic:file",
) -> OutputFile:
    """Creates and returns an OutputFile object.

    Args:
        output_path: The path to the output directory.
        filename: The name of the output file (optional).
        file_extension: The extension of the output file (optional).
        data_type: The data type of the output file (optional).

    Returns:
        An OutputFile object.
    """
    return OutputFile(output_path, filename, file_extension, data_type)
