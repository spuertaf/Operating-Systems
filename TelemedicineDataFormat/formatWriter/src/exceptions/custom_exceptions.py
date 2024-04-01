import traceback
import json


class CapturedException(Exception):
    def __init__(
            self,
            message: str,
            source_error: Exception = None
    ):
        self._message = message
        self._original_error = source_error
        super().__init__(self._message)

    def _get_traceback_info(self) -> list[str]:
        traceback_list = traceback.extract_tb(self._original_error.__traceback__)
        return [
            f"{frame.filename} line {frame.lineno} {frame.name}"
            for frame in traceback_list
        ]

    def _to_dict(self):
        return {
            "message": self._message,
            "source": self._get_traceback_info(),
            "original_error": str(self._original_error)
        }

    def __str__(self):
        return json.dumps(self._to_dict())


class FolderNotFoundException(CapturedException): ...
