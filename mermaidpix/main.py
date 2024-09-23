"""
MermaidPix: Convert Mermaid diagrams in Markdown to high-res PNG images
"""

import click  # Import Click instead of argparse
from mermaidpix.file_processor import (
    process_markdown_file,
)  # Ensure this import is correct

VERSION = "0.7.1"


@click.command()  # Define the command
@click.option(
    "--image-dir",
    type=str,
    default="images",
    help="Directory where the generated PNG images will be stored. Defaults to 'images'.",
)
@click.argument("input_file", type=str, help="Path to the input markdown file.")
@click.argument(
    "output_file", type=str, help="Path to save the processed markdown output."
)
@click.version_option(version=VERSION)  # Version option
def main(input_file: str, output_file: str, image_dir: str) -> None:
    """Main function to process the markdown file."""
    # Call the processing function with the provided arguments
    process_markdown_file(input_file, output_file, image_dir=image_dir)


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    main()
