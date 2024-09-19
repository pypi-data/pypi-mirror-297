from setuptools import setup, find_packages

setup(
    name="big_o_estimator",  # Name of your package
    version="0.1.1",  # Initial release version
    description="A package to estimate Big-O complexity of Python functions.",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",  # If your README is in Markdown
    author="Arghya ",
    author_email="arghyazzz@gmail.com",
    url="https://github.com/amukherjee1991/big_o_estimator_package",  # GitHub repo or project homepage
    packages=find_packages(),  # Automatically find and include the package
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Python version requirement
    include_package_data=True,  # Include additional files (like README.md)
    license="MIT",  # License for your package
)
