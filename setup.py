# setup.py — minimal install_requires (keep package install from local source only)

from pathlib import Path
from setuptools import setup, find_packages

HERE = Path(__file__).parent
readme = (HERE / "README.md").read_text(encoding="utf-8") if (HERE / "README.md").exists() else ""

setup(
    name="ghost",
    version="8.0.0",
    description="Ghost Framework — Android post-exploitation framework (ADB-based).",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/EntySec/Ghost",
    author="EntySec",
    author_email="entysec@gmail.com",
    license="MIT",
    python_requires=">=3.7",
    packages=find_packages(exclude=("tests", "docs", "examples")),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Security",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    # Keep runtime install_requires minimal. Put VCS/complex deps into requirements.txt
    install_requires=[
        "adb-shell",
    ],
    entry_points={
        "console_scripts": [
            "ghost = ghost:cli",
        ]
    },
    project_urls={
        "Source": "https://github.com/EntySec/Ghost",
        "Issues": "https://github.com/EntySec/Ghost/issues",
    },
)
