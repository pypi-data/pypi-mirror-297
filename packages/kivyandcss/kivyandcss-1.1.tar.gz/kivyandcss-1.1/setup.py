from setuptools import setup, find_packages

setup(
    name="kivyandcss",  # Tên thư viện của bạn
    version="1.1",
    author="Bobby",
    author_email="akirasumeragi699@gmail.com",
    description="A CSS-like styling library for Kivy applications",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/hqmdokkai/kivyandcss",  # URL repo của bạn
    packages=find_packages(),
    install_requires=[
        "kivy",  # Các phụ thuộc cần thiết, ở đây là Kivy
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
