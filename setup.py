import setuptools

with open('requirements.txt', 'r') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name='utility',
    version='0.0.3',
    author='Andrew Parry',
    author_email='a.parry.1@research.gla.ac.uk',
    description="Utilities for research",
    url='https://github.com/Parry-Parry/ParryUtil',
    packages=setuptools.find_packages(),
    install_requires=requirements,
    python_requires='>=3.7',
    entry_points={
        'console_scripts': ['utility=utility:main_cli'],
    },
)
