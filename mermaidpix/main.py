"""
MermaidPix: Convert Mermaid diagrams in Markdown to high-res PNG images
"""

import os
import click

from mermaidpix.file_processor import process_markdown_file

VERSION = "0.7.4"


@click.command()  # Define the command
@click.argument("input_file", type=str)  # Removed help parameter
@click.argument("output_file", type=str)  # Removed help parameter
@click.version_option(version=VERSION)  # Version option
def main(input_file: str, output_file: str) -> None:
    """Main function to process the markdown file."""

    # Correctly set the image directory to the directory of the output file
    image_dir = os.path.relpath(os.path.join(os.path.dirname(os.path.abspath(output_file)), "assets"))
    # Call the processing function with the provided arguments
    process_markdown_file(input_file, output_file, image_dir=image_dir)


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    main()
