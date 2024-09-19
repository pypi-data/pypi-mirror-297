from setuptools import setup, find_packages


setup(
    name="sop_voice",
    version = "1.0.1",
    packages=find_packages(),
    include_package_data=True,
    description="Manage voice informations of each sites.",
    author="Leorevoir",
    author_email="leo.quinzler@epitech.eu",
    install_requires=[
        'sop-utils==1.0',
    ],
    classifiers=[
        'Framework :: Django',
        'Programming Language :: Python :: 3',
    ],
)
