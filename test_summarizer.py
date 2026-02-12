import unittest
import subprocess
import os
import shutil
import summarizer
import time

class TestSummarizer(unittest.TestCase):
    def setUp(self):
        self.root_dir = os.getcwd()
        self.test_dir = os.path.join(self.root_dir, "test_repo")
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        os.makedirs(self.test_dir)
        os.chdir(self.test_dir)
        subprocess.run("git init", shell=True, capture_output=True)
        subprocess.run("git config user.email 'test@example.com'", shell=True, capture_output=True)
        subprocess.run("git config user.name 'Test User'", shell=True, capture_output=True)

    def tearDown(self):
        os.chdir(self.root_dir)
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def create_commit(self, filename, content, message, tag=None):
        with open(filename, "w") as f:
            f.write(content)
        subprocess.run(f"git add {filename}", shell=True, capture_output=True)
        subprocess.run(f'git commit -m "{message}"', shell=True, capture_output=True)
        if tag:
            time.sleep(1.1)
            subprocess.run(f"git tag {tag}", shell=True, capture_output=True)

    def test_resolve_tags_no_tags_one_commit(self):
        self.create_commit("file1.txt", "v1", "First commit")
        first_commit = summarizer.get_first_commit()
        old, new = summarizer.resolve_tags(None, None)
        self.assertEqual(new, "HEAD")
        self.assertEqual(old, first_commit)

    def test_resolve_tags_multiple_tags(self):
        self.create_commit("file1.txt", "v1", "First commit", tag="v1.0")
        self.create_commit("file2.txt", "v2", "Second commit", tag="v2.0")

        tags = summarizer.get_tags()
        self.assertEqual(tags[0], "v2.0")

        old, new = summarizer.resolve_tags(None, None)
        self.assertEqual(new, "v2.0")
        self.assertEqual(old, "v1.0")

        old, new = summarizer.resolve_tags("v2.0", None)
        self.assertEqual(new, "v2.0")
        self.assertEqual(old, "v1.0")

        old, new = summarizer.resolve_tags("v1.0", None)
        self.assertEqual(new, "v1.0")
        self.assertEqual(old, summarizer.get_first_commit())

    def test_get_commits_and_files(self):
        self.create_commit("file1.txt", "v1", "First commit", tag="v1.0")
        self.create_commit("file2.txt", "v2", "Second commit", tag="v2.0")

        commits = summarizer.get_commits("v1.0", "v2.0")
        self.assertIn("Second commit", commits)
        self.assertNotIn("First commit", commits)

        files = summarizer.get_changed_files("v1.0", "v2.0")
        self.assertEqual(files, "file2.txt")

    def test_truncate_text(self):
        text = "a" * 100
        truncated = summarizer.truncate_text(text, 50)
        self.assertTrue(len(truncated) > 50)
        self.assertTrue(truncated.startswith("a" * 50))
        self.assertIn("Truncated", truncated)

if __name__ == "__main__":
    unittest.main()
