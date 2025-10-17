"""
Setup script for AI Customer Support Chatbot
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the long description from README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

# Read requirements
requirements = (this_directory / "requirements.txt").read_text(encoding="utf-8").splitlines()
requirements = [r.strip() for r in requirements if r.strip() and not r.startswith("#")]

setup(
    name="ai-customer-support-chatbot",
    version="1.0.0",
    author="Taher Farg",
    author_email="your.email@example.com",
    description="AI-powered customer support chatbot using RAG, Ollama, and ChromaDB",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/AI-Customer-Support-Chatbot",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.13",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.13",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "chatbot=app:main",
            "build-db=scripts.build_vector_db:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.yml", "*.yaml"],
    },
    keywords="ai chatbot rag ollama langchain chromadb nlp customer-support",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/AI-Customer-Support-Chatbot/issues",
        "Source": "https://github.com/yourusername/AI-Customer-Support-Chatbot",
        "Documentation": "https://github.com/yourusername/AI-Customer-Support-Chatbot/tree/main/docs",
    },
)

