from setuptools import setup, find_packages

base_dependencies = [
    "typer==0.4.1",
    "structlog==21.5.0",
]

dev_dependencies = [
    "pytest",
    "flake8",
    "mypy",
    "grpc-stubs",
]

gcp_dependencies = [
    "google-cloud-compute==0.7.0",
]
doc_dependencies = []
aws_dependencies = []

all = dev_dependencies + gcp_dependencies + doc_dependencies + aws_dependencies

setup(
    name="backupmanager",
    version="0.1",
    author="Matthijs Brouns",
    description="...",
    install_requires=base_dependencies,
    extras_require={
        "dev": dev_dependencies,
        "docs": doc_dependencies,
        "aws": aws_dependencies,
        "gcp": gcp_dependencies,
        "all": all,
    },
    entry_points={"console_scripts": ["backupmanager = backupmanager.cli:main"]},
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)
