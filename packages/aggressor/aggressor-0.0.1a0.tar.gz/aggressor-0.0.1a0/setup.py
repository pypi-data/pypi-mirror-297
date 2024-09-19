from setuptools import find_packages, setup

with open("requirements.txt") as f:
    requirements = [l.strip() for l in f.readlines()]

setup(
    name='aggressor',
    url='https://github.com/JosefAlbers/Aggressor',
    py_modules=['aggressor'],
    packages=find_packages(),
    version='0.0.1-alpha',
    readme="README.md",
    author_email="albersj66@gmail.com",
    description="Ultra-minimal autoregressive diffusion model for image generation",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Josef Albers",
    license="Apache License 2.0",
    python_requires=">=3.12.3",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "aggressor = aggressor:main",
        ],
    },
)
