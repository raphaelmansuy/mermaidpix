"""
This module provides functions to process markdown files and convert Mermaid diagrams to PNG images.
"""

import os
import re
import logging
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


def process_markdown_file(input_file: str, output_file: str, *, image_dir: str) -> None:
    """Process a markdown file and save the output to a specified file.

    Args:
        input_file (str): The path to the input markdown file.
        output_file (str): The path to save the processed output.
        image_dir (str): The directory where images are stored.
    """
    # Resolve and expand user paths
    input_file = os.path.abspath(os.path.expanduser(input_file))
    output_file = os.path.abspath(os.path.expanduser(output_file))
    image_dir = os.path.relpath(os.path.expanduser(image_dir))

    validate_input_file(input_file)
    ensure_image_directory(image_dir)

    with open(input_file, "r", encoding="utf-8") as f:
        content = f.read()

    ensure_image_directory(image_dir)

    def replace_mermaid(match: re.Match) -> str:
        """Replace Mermaid code blocks with corresponding PNG images.

        Args:
            match (re.Match): The regex match object containing the Mermaid code.

        Returns:
            str: Markdown string with the image link or original Mermaid code if conversion fails.
        """
        mermaid_code = match.group(1)
        logging.debug("Processing Mermaid diagram:\n%s", mermaid_code)

        image_filename = convert_mermaid_to_png(mermaid_code, image_dir)

        if image_filename:
            return f"\n![Mermaid Diagram]({os.path.relpath(os.path.join(image_dir, image_filename), os.path.dirname(output_file))})\n"
        else:
            logging.warning(
                "Failed to convert Mermaid diagram to PNG. Keeping original Mermaid code."
            )
            return match.group(0)

    # Regex pattern to find Mermaid code blocks
    pattern = r"```mermaid\n(.*?)\n```"

    # Replace Mermaid code blocks with their corresponding PNG images
    new_content = re.sub(pattern, replace_mermaid, content, flags=re.DOTALL)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(new_content)
