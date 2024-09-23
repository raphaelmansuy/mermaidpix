# MermaidPix

## Why MermaidPix?

In the world of technical documentation and diagramming, Mermaid has become an invaluable tool for creating clear, version-controllable diagrams using simple text-based syntax. However, sharing these diagrams outside of Markdown-rendering environments or in high-resolution formats can be challenging.

**MermaidPix** bridges this gap by automatically converting Mermaid diagrams in your Markdown files into high-resolution PNG images. This tool ensures that your diagrams are:

1. Easily shareable in any context.
2. Rendered in high quality for presentations or publications.
3. Consistently generated, allowing for version control of both the diagram code and the resulting image.

## What is MermaidPix?

MermaidPix is a Python-based command-line tool that:

1. Scans Markdown files for Mermaid diagram code blocks.
2. Converts each Mermaid diagram to a high-resolution PNG image.
3. Replaces the Mermaid code in the Markdown with a link to the generated image.
4. Maintains idempotency by generating consistent filenames based on diagram content.

### Key Features

- High-resolution output (4K) with transparent backgrounds.
- Deterministic file naming for easy version control.
- Efficient processing with caching of previously generated images.
- Verbose logging option for detailed conversion information.

## How to Use MermaidPix

### Prerequisites

1. Python 3.7 or higher.
2. pipx (for installing Python applications globally).
3. Poetry (for dependency management and packaging).
4. Mermaid CLI (mmdc).

### Installation

#### Step 1: Install pipx

If you haven't installed pipx yet, you can do so using pip:

```bash
pip install --user pipx
pipx ensurepath
```

Install using Pypi:

```bash
pipx install mermaidpix
```

#### Step 2: Install Poetry

Use pipx to install Poetry:

```bash
pipx install poetry
```

#### Step 3: Install Mermaid CLI

Install Mermaid CLI globally using npm:

```bash
npm install -g @mermaid-js/mermaid-cli
```

#### Step 4: Install MermaidPix

Clone the repository and install MermaidPix using Poetry:

```bash
git clone https://github.com/raphaelmansuy/mermaidpix.git
cd mermaidpix
poetry install
```

This will create a virtual environment and install all the necessary dependencies.

### Usage

To use MermaidPix, you can run it directly through Poetry:

```bash
poetry run python mermaid_pix/main.py <input_file> <output_file> [-v]
```

Alternatively, you can activate the Poetry shell and run the script:

```bash
poetry shell
python mermaid_pix/main.py <input_file> <output_file> [-v]
```

#### Command Line Arguments

- `<input_file>`: Path to the input Markdown file.
- `<output_file>`: Path where the processed Markdown file will be saved.
- `-v` or `--verbose`: (Optional) Enable verbose logging.

### Example

```bash
poetry run python mermaid_pix/main.py docs/architecture.md docs/architecture_with_images.md -v
```

This command will:

1. Read `docs/architecture.md`.
2. Convert any Mermaid diagrams to PNGs and save them in the same directory as the output file.
3. Create a new file `docs/architecture_with_images.md` with image links replacing Mermaid code blocks.
4. Provide verbose output of the conversion process.

### Example Input and Output

**Input Markdown (`input.md`):**

```markdown
# System Architecture

Here's our current system architecture:


graph TD
    A[Client] -->|HTTP Request| B(Load Balancer)
    B -->|Forward| C{Web Server}
    C -->|Query| D[(Database)]
    C -->|Cache| E((Redis))


This diagram shows the basic flow of our system.
```

**After running MermaidPix:**

```bash
poetry run python mermaid_pix/main.py input.md output.md
```

**Output Markdown (`output.md`):**

```markdown
# System Architecture

Here's our current system architecture:

![Mermaid Diagram](images/diagrams/mermaid_<hash>.png)

This diagram shows the basic flow of our system.
```

The Mermaid diagram is now converted to a high-resolution PNG image, making it easily viewable in any Markdown reader or web browser.

## Development

To set up MermaidPix for development:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/mermaidpix.git
   cd mermaidpix
   ```

2. Install dependencies:
   ```bash
   poetry install
   ```

3. Activate the virtual environment:
   ```bash
   poetry shell
   ```

4. Make your changes and run tests:
   ```bash
   poetry run pytest
   ```

## Contributing

We welcome contributions to MermaidPix! Please see our [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to submit pull requests, report issues, or request features.

## License

MermaidPix is released under the MIT License. See the [LICENSE](LICENSE) file for details.