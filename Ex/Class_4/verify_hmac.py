import hashlib
import hmac
import os
import sys
from pathlib import Path

SECRET = "replace-with-a-random-secret-for-this-lab"

def verify_file(filename):
    path = Path(filename)
    content = path.read_bytes()

    marker = b"# HMAC: "
    index = content.rfind(marker)

    if index == -1:
        print(f"{path.name}: CHECK FAILED - HMAC not found")
        return

    csv_data = content[:index]
    stored_signature = content[index + len(marker):].strip().decode("ascii")

    expected_signature = hmac.new(
        SECRET.encode("utf-8"),
        csv_data,
        hashlib.sha256,
    ).hexdigest()

    if hmac.compare_digest(expected_signature, stored_signature):
        print(f"{path.name}: CHECK PASSED")
    else:
        print(f"{path.name}: CHECK FAILED")

if __name__ == "__main__":
    for filename in sys.argv[1:]:
        verify_file(filename)