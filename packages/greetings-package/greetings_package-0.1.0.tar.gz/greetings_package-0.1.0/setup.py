from setuptools import setup, find_packages

setup(
    name="greetings_package",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A simple package to say hello and goodbye in multiple languages",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/greetings_package",  # Replace with your GitHub URL
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[],  # Add dependencies here if needed
)
