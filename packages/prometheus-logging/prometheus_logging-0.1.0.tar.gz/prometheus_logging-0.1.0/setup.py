from setuptools import setup, find_packages

setup(
    name="prometheus_logging",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A simple logging library for ML projects using Prometheus",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/prometheus_logging",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "prometheus_client",
        "psutil",
    ],
)
