"""
MermaidPix: Convert Mermaid diagrams in Markdown to high-res PNG images
"""

import os
import click

from mermaidpix.file_processor import process_markdown_file

VERSION = "0.7.4"


@click.command()  # Define the command
@click.argument("input_file", type=str)  # Added help parameter
@click.argument("output_file", type=str)  # Added help parameter
@click.version_option(version=VERSION)  # Version option
def main(input_file: str, output_file: str) -> None:
    """Main function to process the markdown file."""
    
    try:
        # Correctly set the image directory to the directory of the output file
        image_dir = os.path.relpath(os.path.join(os.path.dirname(os.path.abspath(output_file)), "assets"))
        print(f"Processing '{input_file}' and saving to '{output_file}'...")  # User feedback
        # Call the processing function with the provided arguments
        process_markdown_file(input_file, output_file, image_dir=image_dir)
        print("Processing completed successfully.")  # User feedback
    except FileNotFoundError as e:
        print(f"Error: {e}. Please check the input file path.")  # Error handling
    # pylint: disable=broad-exception-caught
    except Exception as e:
        print(f"An unexpected error occurred: {e}")  # General error handling


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    main()
