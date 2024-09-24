from setuptools import setup, find_packages

setup(
    name="vishwa_demo_package",
    version="0.1.0",
    author="vishwa",
    author_email="vishwa.automationhub@gmail.com",
    description="A short description of your package",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    #url="https://github.com/yourusername/yourrepo",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
