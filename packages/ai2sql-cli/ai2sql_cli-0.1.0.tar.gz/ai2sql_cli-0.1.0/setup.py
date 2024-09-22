from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ai2sql-cli",
    version="0.1.0",
    author="Mustafa Ergisi",
    author_email="support@ai2sql.io",
    description="A CLI tool for converting natural language to SQL using AI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mergisi/ai2sql-cli",
    packages=find_packages(),
    install_requires=[
        "openai>=1.0.0",
        "sqlalchemy>=1.4.0",
        "mysql-connector-python>=8.0.0",
    ],
    entry_points={
        'console_scripts': [
            'ai2sql=ai2sql.cli:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)