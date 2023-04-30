from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = []

setup(
    name="gpt_guard",
    version="1.0.1",
    author="Walter Haydock",
    author_email="walter@deploy-securely.com",
    description="A lightweight library to sanitize data provided to AI tools",
    long_description="README.md",
    long_description_content_type="text/markdown",
    url="https://github.com/Deploying-Securely/GPT-Guard",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=['License :: OSI Approved :: Apache Software License'],
)
