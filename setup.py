from setuptools import setup

setup(
    name="hackrack-wordlist",
    version="2.0.0",
    description="HackRack Wordlist Generator — interactive wordlist generation for penetration testing",
    author="Ahsan Ahmad Raheel",
    license="MIT",
    py_modules=["main"],
    python_requires=">=3.10",
    entry_points={
        "console_scripts": [
            "hackrack-wordlist=main:main",
        ],
    },
)
