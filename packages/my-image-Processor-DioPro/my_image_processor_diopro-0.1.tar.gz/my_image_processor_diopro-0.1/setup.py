from setuptools import setup, find_packages # type: ignore

setup(
    name="my_image_Processor_DioPro",
    version="0.1",
    packages=find_packages(),
    install_requires=["Pillow"],
    description="A simple image processing library",
    author="Leo",
    author_email="leozzinho12397@gmail.com",
    keywords="image_processing"
)