from setuptools import setup, find_packages

setup(
    name="my_sql_library",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[],
    description="A simple Python library for managing SQL queries",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="palanm5",
    author_email="madhavan.palani@dell.com",
    url="https://github.com/yourusername/my_sql_library",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
