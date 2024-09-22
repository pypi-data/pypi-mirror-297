from setuptools import setup, find_packages

setup(
    name="jgwillhub",
    version="0.1.5",
    description="A prompt template hub helper for langchainhub",
    author="JGWill",
    author_email="jgi@jgwill.com",
    url="https://github.com/jgwill/hub",
    packages=find_packages(),
    install_requires=[
        "requests",  
        "langchainhub"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            'jhub= jgwillhub.cli:main',
        ],
    },
)
