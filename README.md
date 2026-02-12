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

## Global Installation (Recommended)

To use the `git-qa` command from anywhere on your system:

1. Clone this repository.
2. Navigate to the repository root.
3. Install the package globally:
   ```bash
   pip install .
   ```
   *(Note: Use `pip install --break-system-packages .` if you are on a recent macOS/Linux and not using a virtual environment, or simply install it within your preferred global python environment.)*

4. Set your OpenAI API key in your shell profile (`.bashrc`, `.zshrc`, etc.):
   ```bash
   export OPENAI_API_KEY='your-api-key-here'
   ```

Now you can run `git-qa` in any Git repository!

## Alternative Usage

### Run without installation
If you don't want to install it globally, you can run it directly:
```bash
python3 /path/to/summarizer.py [new_tag] [old_tag]
```

### Using a Shell Alias
Add this to your shell profile:
```bash
alias git-qa='python3 /absolute/path/to/summarizer.py'
```

## Usage Examples

Inside any Git repository:

### 1. Compare the latest two tags
```bash
git-qa
```

### 2. Compare a specific tag against its predecessor
```bash
git-qa v2.0
```

### 3. Compare two specific tags or hashes
```bash
git-qa v2.0 v1.0
```

### 4. Adjust character limits for large diffs
```bash
git-qa --max-chars 20000
```

## Output

The tool generates a file named `what_to_qa.md` in the directory where it is executed.

## Running Tests

To verify the logic:
```bash
python3 test_summarizer.py
```
