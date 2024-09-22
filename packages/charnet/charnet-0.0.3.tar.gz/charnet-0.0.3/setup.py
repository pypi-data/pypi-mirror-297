from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='charnet',
    version='0.0.3',
    description='Character interaction temporal graph analysis',
    package_dir={'': 'charnet'},
    packages=find_packages(where="charnet"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/MediaCompLab/CharNet',
    author='Media Comprehension Lab',
    author_email='shu13@gsu.edu',
    license='GPL-3.0',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'pandas',
        'networkx',
        'numpy',
        'matplotlib'
    ],
    extras_require={
        'all': ['plotly', 'gravis', 'pyvis'],
        'dev': ['pytest>=7.0', 'twine>=4.0.2']
    },
    python_requires='>=3.6',
)
