from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()


with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name='DRRTools',
    version='0.0.1',
    author="Douglas R. Ramos",
    author_email="douglaspro.business@gmail.com",
    description='My short description/Minha curta descrição',
    long_description=page_description,
    long_description_content_type='text/markdown',
    url='https://github.com/DouglasRR/DRRTools',
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)