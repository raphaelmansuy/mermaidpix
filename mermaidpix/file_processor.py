"""
This module provides functions to process markdown files and convert Mermaid diagrams to PNG images.
"""

import os
import logging
import re
from mermaidpix.mermaid_converter import convert_mermaid_to_png

def validate_input_file(input_file: str) -> None:
    """Validate the input file existence.

    Args:
        input_file (str): The path to the input markdown file.

    Raises:
        FileNotFoundError: If the input file does not exist.
    """
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")

def ensure_image_directory(image_dir: str) -> None:
    """Ensure the image directory exists.

    Args:
        image_dir (str): The directory where images are stored.
    """
    os.makedirs(image_dir, exist_ok=True)

def process_markdown_file(input_file: str, output_file: str, image_dir: str) -> None:
    """Process a markdown file and save the output to a specified file.

    Args:
        input_file (str): The path to the input markdown file.
        output_file (str): The path to save the processed output.
        image_dir (str): The directory where images are stored.
    """
    with open(input_file, "r", encoding="utf-8") as f:
        content = f.read()

    ensure_image_directory(image_dir)

    def replace_mermaid(match: re.Match) -> str:
        mermaid_code = match.group(1)
        logging.debug("Processing Mermaid diagram:\n%s", mermaid_code)
        image_filename = convert_mermaid_to_png(mermaid_code, image_dir)
        if image_filename:
            return f"\n![Mermaid Diagram]({os.path.join(image_dir, image_filename)})\n"
        else:
            logging.warning(
                "Failed to convert Mermaid diagram to PNG. Keeping original Mermaid code."
            )
            return match.group(0)

    pattern = r"```mermaid\n(.*?)\n```"
    new_content = re.sub(pattern, replace_mermaid, content, flags=re.DOTALL)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(new_content)