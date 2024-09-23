from setuptools import setup, find_packages

setup(
    name="babyagi",
    version="0.0.2",  # Temporary version
    author="Yohei Nakajima",
    author_email="babyagi@untapped.vc",
    description="Temporary description for babyagi package.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yoheinakajima/babyagi",  # Placeholder URL
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
