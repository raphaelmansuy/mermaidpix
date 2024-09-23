"""
MermaidPix: Convert Mermaid diagrams in Markdown to high-res PNG images
"""

from typing import Optional  # Import Optional for type hinting
import logging  # Import logging for logging functionality

import click  # Import Click for argument parsing
from mermaidpix.logger import setup_logging
from mermaidpix.file_processor import validate_input_file, process_markdown_file


@click.command()
@click.argument("input_file")
@click.argument("output_file")
@click.option(
    "--image-dir",
    default="asset",
    help="Directory to store generated images (default: 'asset')",
)
@click.option(
    "-o", "--output", help="Output Markdown file (overwrites the existing file)"
)
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose logging")
def main(
    input_file: str,
    output_file: str,
    image_dir: str,
    output: Optional[str],
    verbose: bool,
) -> None:
    """Main entry point for the MermaidPix application.

    Converts Mermaid diagrams in Markdown to high-resolution PNG images.
    """
    setup_logging(verbose)

    try:
        validate_input_file(input_file)
        logging.info("Processing input file: %s", input_file)

        # Use the --output argument if provided, otherwise use the positional output_file
        output_file = output if output else output_file

        process_markdown_file(input_file, output_file, image_dir)
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
    # Provide the necessary arguments for the main function
    # pylint: disable=no-value-for-parameter
    main()  # Example arguments
