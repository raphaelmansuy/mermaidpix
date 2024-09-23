"""
This module provides functions to process markdown files and convert Mermaid diagrams to PNG images.
"""

import os
import subprocess
import hashlib
import logging
import time
from typing import Optional


def get_deterministic_filename(mermaid_code: str) -> str:
    """
    Generates a deterministic filename for a given Mermaid code.

    Args:
        mermaid_code (str): The Mermaid code for which the filename is generated.

    Returns:
        str: The deterministic filename in the format 'mermaid_{hash}.png', where
              'hash' is the first 16 characters of the MD5 hash of the Mermaid code.
    """
    hash_object = hashlib.md5(mermaid_code.encode())
    hash_hex = hash_object.hexdigest()
    return f"mermaid_{hash_hex[:16]}.png"


def convert_mermaid_to_png(
    mermaid_code: str, output_dir: str, dpi: int = 300
) -> Optional[str]:
    """
    Converts a Mermaid diagram code to a PNG image.

    Args:
        mermaid_code (str): The Mermaid diagram code to convert.
        output_dir (str): The directory where the PNG image will be saved.
        dpi (int, optional): The DPI (dots per inch) of the output image. Defaults to 300.

    Returns:
        Optional[str]: The filename of the converted PNG image if successful, None otherwise.
    """
    filename = get_deterministic_filename(mermaid_code)
    output_path = os.path.join(output_dir, filename)

    if os.path.exists(output_path):
        logging.debug("Image already exists, skipping conversion: %s", output_path)
        return filename

    temp_file = f"temp_{hashlib.md5(mermaid_code.encode()).hexdigest()[:8]}.mmd"

    with open(temp_file, "w", encoding="utf-8") as f:  # Specify encoding
        f.write(mermaid_code)

    logging.debug("Converting Mermaid diagram to PNG: %s -> %s", temp_file, output_path)

    try:
        start_time = time.time()
        process = subprocess.Popen(
            [
                "mmdc",
                "-i",
                temp_file,
                "-o",
                output_path,
                "-b",
                "transparent",
                "-w",
                "3840",
                "-H",
                "2160",  # 4K resolution
                "-s",
                "4",
            ],  # Scale factor
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        stdout, stderr = process.communicate(timeout=60)  # 60 seconds timeout
        logging.info(
            "Process output: %s", stdout
        )  # Log the stdout using lazy formatting

        if process.returncode != 0:
            logging.error("Error converting Mermaid to PNG: %s", stderr)
            return None

        end_time = time.time()
        logging.debug("Conversion completed in %.2f seconds", end_time - start_time)

    except subprocess.TimeoutExpired:
        logging.error("Mermaid conversion timed out after 60 seconds")
        process.kill()
        return None

    # pylint: disable=broad-exception-caught
    except Exception as e:
        logging.error("Unexpected error during Mermaid conversion: %s", str(e))
        return None

    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)

    return filename
