from setuptools import setup, find_packages

setup(
    name="kern-engine",
    version="0.1.0",
    description="A deep-reloading development engine for Python",
    author="Emmanuel Obolo Oluwapelumi & Abiodun Kumuyi",
    packages=find_packages(include=["kern", "kern.*"]),
    entry_points={
        "console_scripts": [
            "kern=kern.core.main:main",
        ],
    },
)
