import argparse
import subprocess
import os
import sys
from openai import OpenAI

def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        return None
    return result.stdout.strip()

def get_tags():
    tags = run_command("git tag --sort=-creatordate")
    if not tags:
        return []
    return tags.split('\n')

def get_first_commit():
    return run_command("git rev-list --max-parents=0 HEAD")

def get_commits(old, new):
    return run_command(f"git log {old}..{new} --oneline")

def get_changed_files(old, new):
    return run_command(f"git diff {old}..{new} --name-only")

def resolve_tags(args_new, args_old):
    tags = get_tags()
    new_tag = args_new
    old_tag = args_old

    if not new_tag:
        if len(tags) >= 1:
            new_tag = tags[0]
        else:
            new_tag = "HEAD"

    if not old_tag:
        if new_tag in tags:
            idx = tags.index(new_tag)
            if idx + 1 < len(tags):
                old_tag = tags[idx+1]
            else:
                old_tag = get_first_commit()
        else:
            if len(tags) >= 1:
                old_tag = tags[0]
            else:
                old_tag = get_first_commit()

    return old_tag, new_tag

def main():
    parser = argparse.ArgumentParser(description="Summarize git commits between tags and identify QA tasks.")
    parser.add_argument("new_tag", nargs='?', help="The new tag (default: latest tag)")
    parser.add_argument("old_tag", nargs='?', help="The old tag (default: tag before new_tag)")

    args = parser.parse_args()

    try:
        old_tag, new_tag = resolve_tags(args.new_tag, args.old_tag)
    except Exception as e:
        print(f"Error resolving tags: {e}")
        sys.exit(1)

    if not old_tag or not new_tag:
         print("Error: Could not determine range to compare.")
         sys.exit(1)

    if old_tag == new_tag:
        print(f"Comparing {old_tag} to {new_tag} (same reference).")
        commits = run_command(f"git log -1 {new_tag} --oneline")
        files = run_command(f"git show --name-only --format='' {new_tag}")
    else:
        print(f"Comparing {old_tag} to {new_tag}...")
        commits = get_commits(old_tag, new_tag)
        files = get_changed_files(old_tag, new_tag)

    if not commits:
        print("No commits found between specified tags/commits.")
        return

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable is not set.")
        # In a real scenario we'd exit, but for testing purposes we might want to see the gathered data
        print(f"Commits:\n{commits}")
        print(f"Files:\n{files}")
        sys.exit(1)

    client = OpenAI(api_key=api_key)

    prompt = f"""
Summarize the following git commits and identify what should be checked during QA.
Return the output in Markdown format.

Commits:
{commits}

Changed Files:
{files}

The output should have two sections:
1. Commit Summary: A concise summary of the changes.
2. QA Recommendations: A list of specific areas or scenarios to test based on the modified files and commit messages. Identify both "what" to test and "how" (based on files changed).
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes code changes and provides QA guidance."},
                {"role": "user", "content": prompt}
            ]
        )

        output = response.choices[0].message.content

        with open("what_to_qa.md", "w") as f:
            f.write(output)

        print("Summary and QA recommendations written to what_to_qa.md")

    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
