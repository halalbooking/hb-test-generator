from setuptools import setup, find_packages

setup(
    name="hb_test_generator",
    version="0.1.0",
    description="A package to generate tests & write it into files using OpenAI's GPT-3",
    author="Maksymenkov Eugene",
    author_email="foatei@gmail.com",
    url="https://github.com/halalbooking/hb_test_generator",
    packages=find_packages(),
    install_requires=[
        "openai",
    ],
    entry_points={
        "console_scripts": [
            "hb_generate_tests=hb_test_generator.generate_tests:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
