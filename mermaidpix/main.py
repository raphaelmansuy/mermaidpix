"""
MermaidPix: Convert Mermaid diagrams in Markdown to high-res PNG images
"""

import re
import subprocess
import os
import hashlib
import argparse
import logging
import time
import shutil

from typing import Optional


def setup_logging(verbose: bool) -> None:
    """
    Set up logging configuration.

    Args:
        verbose (bool): If True, set the logging level to DEBUG. If False, set it to INFO.

    Returns:
        None
    """
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level, format="%(asctime)s - %(levelname)s - %(message)s")


def check_mermaid_cli() -> bool:
    """
    Checks if Mermaid CLI (mmdc) is installed and in the system PATH.

    Returns:
        bool: True if Mermaid CLI is installed, False otherwise.
    """
    if shutil.which("mmdc") is None:
        logging.error("Mermaid CLI (mmdc) is not installed or not in the system PATH.")
        logging.info("To install Mermaid CLI, follow these steps:")
        logging.info("1. Ensure you have Node.js installed (https://nodejs.org/)")
        logging.info("2. Run the following command:")
        logging.info("   npm install -g @mermaid-js/mermaid-cli")
        logging.info("3. After installation, restart your terminal or command prompt.")
        logging.info(
            "For more information, visit: https://github.com/mermaid-js/mermaid-cli"
        )
        return False
    return True


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
                "4",  # Scale factor
                "-d",  # DPI option
                str(dpi),  # Use the dpi argument
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        stdout, stderr = process.communicate(timeout=60)  # 60 seconds timeout
        logging.info("Process output: %s", stdout)  # Log the stdout using lazy formatting

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


def process_markdown_file(input_file: str, output_file: str, image_dir: str) -> None:
    """Process a markdown file and save the output to a specified file.

    Args:
        input_file (str): The path to the input markdown file.
        output_file (str): The path to save the processed output.
        image_dir (str): The directory where images are stored.
    """
    with open(input_file, "r", encoding="utf-8") as f:
        content = f.read()

    os.makedirs(image_dir, exist_ok=True)

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


def main() -> None:
    """Main entry point for the MermaidPix application.

    Converts Mermaid diagrams in Markdown to high-resolution PNG images.
    """
    parser = argparse.ArgumentParser(
        description="MermaidPix: Convert Mermaid diagrams in Markdown to high-res PNG images"
    )
    parser.add_argument("input_file", help="Input Markdown file")
    parser.add_argument("output_file", help="Output Markdown file")
    parser.add_argument("image_dir", nargs='?', default="asset", help="Directory to store generated images (default: 'asset')")
    parser.add_argument(
        "-o", "--output", help="Output Markdown file (overwrites the existing file)"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose logging"
    )
    args = parser.parse_args()

    setup_logging(args.verbose)

    if not check_mermaid_cli():
        exit(1)

    try:
        if not os.path.exists(args.input_file):
            raise FileNotFoundError(f"Input file not found: {args.input_file}")

        logging.info("Processing input file: %s", args.input_file)
        
        # Use the --output argument if provided, otherwise use the positional output_file
        output_file = args.output if args.output else args.output_file
        
        # Ensure the image directory exists
        os.makedirs(args.image_dir, exist_ok=True)
        
        process_markdown_file(args.input_file, output_file, args.image_dir)
        logging.info("Processing complete. Output written to %s", output_file)
    except FileNotFoundError as e:
        logging.error("%s", str(e))
        exit(1)
    except PermissionError:
        logging.error("Permission denied when accessing files or directories.")
        exit(1)
    # pylint: disable=broad-exception-caught
    except Exception as e:
        logging.error("An unexpected error occurred: %s", str(e))
        exit(1)


if __name__ == "__main__":
    main()
