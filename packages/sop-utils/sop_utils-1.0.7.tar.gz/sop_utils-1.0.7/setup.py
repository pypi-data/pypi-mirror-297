from setuptools import setup, find_packages


setup(
    name="sop_utils",
    version='1.0.7',
    packages=find_packages(),
    include_package_data=True,
    description="Utilities for the SOP Netbox Plugins.",
    author="Leorevoir",
    author_email="leo.quinzler@epitech.eu",
    classifiers=[
        'Framework :: Django',
        'Programming Language :: Python :: 3',
    ],
    zip_safe=False,
)
