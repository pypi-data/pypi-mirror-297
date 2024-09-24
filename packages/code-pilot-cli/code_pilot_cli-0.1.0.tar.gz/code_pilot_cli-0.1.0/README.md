# Code Pilot CLI

[![Continuous Integration](https://github.com/youzarsiph/code-pilot-cli/actions/workflows/ci.yml/badge.svg)](https://github.com/youzarsiph/code-pilot-cli/actions/workflows/ci.yml)
[![Continuous Deployment](https://github.com/youzarsiph/code-pilot-cli/actions/workflows/cd.yml/badge.svg)](https://github.com/youzarsiph/code-pilot-cli/actions/workflows/cd.yml)
[![Black](https://github.com/youzarsiph/code-pilot-cli/actions/workflows/black.yml/badge.svg)](https://github.com/youzarsiph/code-pilot-cli/actions/workflows/black.yml)
[![Ruff](https://github.com/youzarsiph/code-pilot-cli/actions/workflows/ruff.yml/badge.svg)](https://github.com/youzarsiph/code-pilot-cli/actions/workflows/ruff.yml)

Your customizable coding assistant for the command line interface (CLI).

## Demo

<iframe width="560" height="315" src="https://www.youtube.com/embed/VWiPISA9rKo?si=rW6ute2QXwq5KevI" title="YouTube Video Demonstration" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

## Getting Started

To begin, clone the repository:

```bash
git clone https://github.com/youzarsiph/code-pilot-cli
cd code-pilot-cli
```

Next, install the required dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file and include your `HF_TOKEN`:

```bash
# Create the file
touch .env
```

Open the file in your preferred text editor:

```bash
HF_TOKEN=hf_**********************************
```

Alternatively, you may export your `HF_TOKEN` as an environment variable:

```bash
export HF_TOKEN=hf_**********************************
```

Install Poetry for dependency management:

```bash
pip install poetry
```

Build and install the project:

```bash
poetry build
poetry install
```

You are now ready to utilize the application.

## Usage

To view the help options, run:

```bash
code-pilot --help
```

### Generate Commands

You can generate shell commands using natural language:

```bash
code-pilot ai 'list all files in the current directory'
```

### Chat

Engage in a chat with CodePilot:

```bash
code-pilot chat

# Custom system message
code-pilot chat -sm 'You are a helpful assistant'

# Export chat history
code-pilot chat -e chat-history.json

# Import chat history
code-pilot chat -h chat-history.json

# Import chat history and then export it after the session
code-pilot chat -h chat-history.json -e chat-history.json
```

### Code Completions

Receive code completions from CodePilot:

```bash
code-pilot completions 'fn add(x: i32, y: i32) -> i32 {'
```

### Code Enhancements

Obtain suggestions from CodePilot for improving your code to adhere to best practices and industry standards:

```bash
code-pilot enhance app.py
```

### Perform Code Scans

Check your code for potential security vulnerabilities:

```bash
code-pilot scan app.py
```

### Custom Large Language Models (LLMs)

Utilize custom LLMs:

```bash
code-pilot chat -m 'mistralai/Mistral-Nemo-Instruct-2407'
```

## License

This project is licensed under the MIT License.
