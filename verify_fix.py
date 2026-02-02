
import sys
import os
from faster_whisper import WhisperModel

# Mocking WhisperModel to avoid 3GB download during test if possible,
# OR just verifying the call signature.
# actually faster-whisper will start downloading immediately.
# Let's just check if the syntax is valid by checking the file content via grep/ast
# or trusting the edit.
# But for "Verification", I can try to instantiate it with a "tiny" model as a proxy test
# if I change the code temporarily? No, that's invasive.

# Let's create a script that IMPORTS the service and checks the class definition or partial init?
# Ideally we run the real code.
# Since I cannot download 3GB easily here without waiting forever,
# I will verify by code inspection and perhaps a small unit test that mocks WhisperModel
# to ensure the arguments are passed correctly.

from unittest.mock import patch, MagicMock
from backend.service import TranscriptionService


@patch("backend.service.WhisperModel")
def test_service_init(mock_whisper):
    print("Testing Service Init...")
    service = TranscriptionService()

    # Check if called correctly
    mock_whisper.assert_called_with(
        "large-v3",
        device="cuda",
        compute_type="float16",
        download_root="../modelo_whisper"  # Default val in service.py init
    )
    print("SUCCESS: Service initialized with correct download_root args.")


if __name__ == "__main__":
    try:
        test_service_init()
    except Exception as e:
        print(f"FAIL: {e}")
        sys.exit(1)
