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
- An OpenAI API Key

## Installation

1. Clone the repository (if not already done).
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set your OpenAI API key as an environment variable:
   ```bash
   export OPENAI_API_KEY='your-api-key-here'
   ```

## Usage

Run the script from the root of your git repository:

### 1. Compare the latest two tags
```bash
python3 summarizer.py
```

### 2. Compare a specific tag against its predecessor
```bash
python3 summarizer.py v2.0
```

### 3. Compare two specific tags or hashes
```bash
python3 summarizer.py v2.0 v1.0
```

## Output

The tool generates a file named `what_to_qa.md` in the current directory, containing:
1. **Commit Summary**: A high-level overview of the changes.
2. **QA Recommendations**: A list of specific test scenarios and areas of focus.

## Running Tests

To verify the tag resolution and git integration logic:
```bash
python3 test_summarizer.py
```
