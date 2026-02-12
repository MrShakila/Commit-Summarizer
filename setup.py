from setuptools import setup

setup(
    name="git-qa-summarizer",
    version="1.0.0",
    py_modules=["summarizer"],
    install_requires=[
        "openai",
    ],
    entry_points={
        "console_scripts": [
            "git-qa=summarizer:main",
        ],
    },
)
