import re
import subprocess
import os
import hashlib
import argparse
import logging
import time
import shutil

def setup_logging(verbose):
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level, format="%(asctime)s - %(levelname)s - %(message)s")

def check_mermaid_cli():
    if shutil.which("mmdc") is None:
        print("Mermaid CLI (mmdc) is not installed or not in the system PATH.")
        print("To install Mermaid CLI, follow these steps:")
        print("1. Ensure you have Node.js installed (https://nodejs.org/)")
        print("2. Run the following command:")
        print("   npm install -g @mermaid-js/mermaid-cli")
        print("3. After installation, restart your terminal or command prompt.")
        print("For more information, visit: https://github.com/mermaid-js/mermaid-cli")
        return False
    return True

def get_deterministic_filename(mermaid_code):
    hash_object = hashlib.md5(mermaid_code.encode())
    hash_hex = hash_object.hexdigest()
    return f"mermaid_{hash_hex[:16]}.png"

def convert_mermaid_to_png(mermaid_code, output_dir, dpi=300):
    filename = get_deterministic_filename(mermaid_code)
    output_path = os.path.join(output_dir, filename)

    if os.path.exists(output_path):
        logging.debug(f"Image already exists, skipping conversion: {output_path}")
        return filename

    temp_file = f"temp_{hashlib.md5(mermaid_code.encode()).hexdigest()[:8]}.mmd"
    with open(temp_file, "w") as f:
        f.write(mermaid_code)

    logging.debug(f"Converting Mermaid diagram to PNG: {temp_file} -> {output_path}")

    try:
        start_time = time.time()
        process = subprocess.Popen(
            [
                "mmdc",
                "-i", temp_file,
                "-o", output_path,
                "-b", "transparent",
                "-w", "3840",
                "-H", "2160",  # 4K resolution
                "-s", "4",  # Scale factor
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        stdout, stderr = process.communicate(timeout=60)  # 60 seconds timeout

        if process.returncode != 0:
            logging.error(f"Error converting Mermaid to PNG: {stderr}")
            return None

        end_time = time.time()
        logging.debug(f"Conversion completed in {end_time - start_time:.2f} seconds")

    except subprocess.TimeoutExpired:
        logging.error("Mermaid conversion timed out after 60 seconds")
        process.kill()
        return None
    except Exception as e:
        logging.error(f"Unexpected error during Mermaid conversion: {str(e)}")
        return None
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)

    return filename

def process_markdown_file(input_file, output_file, image_dir):
    with open(input_file, "r") as f:
        content = f.read()

    os.makedirs(image_dir, exist_ok=True)

    def replace_mermaid(match):
        mermaid_code = match.group(1)
        logging.debug(f"Processing Mermaid diagram:\n{mermaid_code}")
        image_filename = convert_mermaid_to_png(mermaid_code, image_dir)
        if image_filename:
            return f"\n![Mermaid Diagram]({os.path.join(image_dir, image_filename)})\n"
        else:
            logging.warning(f"Failed to convert Mermaid diagram to PNG. Keeping original Mermaid code.")
            return match.group(0)

    pattern = r"```mermaid\n(.*?)\n```"
    new_content = re.sub(pattern, replace_mermaid, content, flags=re.DOTALL)

    with open(output_file, "w") as f:
        f.write(new_content)

def main():
    parser = argparse.ArgumentParser(description="MermaidPix: Convert Mermaid diagrams in Markdown to high-res PNG images")
    parser.add_argument("input_file", help="Input Markdown file")
    parser.add_argument("output_file", help="Output Markdown file")
    parser.add_argument("image_dir", help="Directory to store generated images")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging")
    args = parser.parse_args()

    setup_logging(args.verbose)

    if not check_mermaid_cli():
        exit(1)

    try:
        if not os.path.exists(args.input_file):
            raise FileNotFoundError(f"Input file not found: {args.input_file}")

        logging.info(f"Processing input file: {args.input_file}")
        process_markdown_file(args.input_file, args.output_file, args.image_dir)
        logging.info(f"Processing complete. Output written to {args.output_file}")
    except FileNotFoundError as e:
        logging.error(str(e))
        exit(1)
    except PermissionError:
        logging.error(f"Permission denied when accessing files or directories.")
        exit(1)
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()