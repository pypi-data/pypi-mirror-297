from setuptools import setup, find_packages

setup(
    name="component_reuse",
    version="0.5.0",
    packages=find_packages(),
    install_requires=[
        "pika",
    ],
    author="Your Name",
    description="Reusable RabbitMQ Adapter for Multiple Services",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/component-reuse",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
