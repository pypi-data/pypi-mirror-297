from setuptools import find_packages, setup

# Last update: 2023-10-01
setup(
    name="speedy-utils",
    version="v1.0.2",
    description="Fast and easy-to-use package for data science",
    author="AnhVTH",
    author_email="anhvth.226@gmail.com",
    url="https://github.com/anhvth/speedy",
    packages=find_packages(),  # Automatically find all packages in the directory
    install_requires=[  # List any dependencies your package requires
        "numpy",
        "requests",
        "xxhash",
        "loguru",
        "fastcore",
        "debugpy",
        "ipywidgets",
        "jupyterlab",
        "ipdb",
        "scikit-learn",
        "matplotlib",
        "pandas",
        "tabulate",
        "pydantic",
    ],
)
