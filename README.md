# Git Commit Summarizer & QA Identifier

A Python CLI tool that summarizes git commits between two tags (or references) and identifies specific areas for QA testing using OpenAI's GPT-4o.

## Features

- **Automated Summarization**: Summarizes commit messages into a concise readable format.
- **QA Recommendations**: Suggests what to test and how, based on both commit messages and the files that were changed.
- **Smart Tag Resolution**:
  - No arguments: Compares the two most recent tags.
  - One argument (`new_tag`): Compares the specified tag against the one immediately preceding it.
  - Two arguments (`new_tag`, `old_tag`): Compares the range between the two specified tags.
- **Token Management**: Automatically truncates input if it's too large to fit within OpenAI's rate limits.
- **Customizable Limits**: Use the `--max-chars` flag to adjust the amount of data sent to the API.

## Prerequisites

- Python 3.x
- Git
- An OpenAI API Key (`OPENAI_API_KEY` environment variable)

## Installation

### 1. Install Dependencies
The tool requires the `openai` Python package. You must install it in your Python environment:
```bash
pip install openai
```
*Note: If you are using a virtual environment, ensure it is activated before installing.*

### 2. Set OpenAI API Key
```bash
export OPENAI_API_KEY='your-api-key-here'
```

## Usage

### Basic usage
```bash
python3 summarizer.py [new_tag] [old_tag]
```

### Handling large diffs
If you encounter "Rate Limit Exceeded" errors, you can reduce the amount of data sent:
```bash
python3 summarizer.py --max-chars 20000
```

### In a different Git project
Navigate to the root of your other project and run:
```bash
python3 /path/to/summarizer.py [new_tag] [old_tag]
```
**Important:** Ensure that the environment where you run the command has the `openai` package installed.

## Output

The tool generates a file named `what_to_qa.md` in the directory where it is executed.

## Running Tests

To verify the logic:
```bash
python3 test_summarizer.py
```
