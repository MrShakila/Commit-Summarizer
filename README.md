# Git Commit Summarizer & QA Identifier

A Python CLI tool that summarizes git commits between two tags (or references) and identifies specific areas for QA testing using OpenAI's GPT-4o.

## Features

- **Automated Summarization**: Summarizes commit messages into a concise readable format.
- **QA Recommendations**: Suggests what to test and how, based on both commit messages and the files that were changed.
- **Smart Tag Resolution**:
  - No arguments: Compares the two most recent tags.
  - One argument (`new_tag`): Compares the specified tag against the one immediately preceding it.
  - Two arguments (`new_tag`, `old_tag`): Compares the range between the two specified tags.
  - Handles repositories with no tags by falling back to the first commit.

## Prerequisites

- Python 3.x
- Git
- An OpenAI API Key (`OPENAI_API_KEY` environment variable)

## Installation

1. Install the required dependencies:
   ```bash
   pip install openai
   ```
2. Set your OpenAI API key:
   ```bash
   export OPENAI_API_KEY='your-api-key-here'
   ```

## Usage

### In this repository
Run the script from the root:
```bash
python3 summarizer.py [new_tag] [old_tag]
```

### In a different Git project
You can use this tool in any Git repository by following these steps:

#### Option 1: Run by providing the path
Navigate to the root of your other project and run:
```bash
python3 /path/to/summarizer.py [new_tag] [old_tag]
```

#### Option 2: Copy the script
Simply copy `summarizer.py` to the root of your other project and run it there.

#### Option 3: Global Alias
Add an alias to your `.bashrc` or `.zshrc`:
```bash
alias git-qa='python3 /absolute/path/to/summarizer.py'
```
Then you can just run `git-qa` inside any git repo.

## Output

The tool generates a file named `what_to_qa.md` in the directory where it is executed.

## Running Tests

To verify the tag resolution and git integration logic:
```bash
python3 test_summarizer.py
```
