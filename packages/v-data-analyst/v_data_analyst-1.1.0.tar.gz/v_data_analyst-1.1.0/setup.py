from setuptools import setup, find_packages

setup(
    name="v-data-analyst",  # Replace with your package name
    version="1.1.0",
    description="Basic Understanding of publishing packages to the PYpi",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    #url="https://github.com/yourusername/your-repo",  # Optional, your project's URL
    author="Vishwanath",
    author_email="vishwa.automationhub@gmail.com",
    license="MIT",  # Use your preferred license
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Minimum Python version
)
