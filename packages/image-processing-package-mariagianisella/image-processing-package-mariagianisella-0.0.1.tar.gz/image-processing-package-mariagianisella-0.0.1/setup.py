from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="image-processing-package-mariagianisella",
    version="0.0.1",
    author="maria-gianisella",
    author_email="maria.ggianisella@gmail.com",
    description="Python package of image processing",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/maria-gianisella/image-processing-package",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)