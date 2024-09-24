from setuptools import setup, find_packages

setup(
    name="qda_package",
    version="1.0.2",
    packages=find_packages(),
    include_package_data=True,  # Include all data files (important for including pytransform)
    package_data={
        "qda_package": ["pytransform/*"],  # Include all files in the pytransform directory
    },
    install_requires=[  # List of dependencies
        "requests==2.31.0",
        "psutil==6.0.0",
        "GPUtil==1.4.0"
    ],
    description="An obfuscated Python package containing ParentInterface",
    author="Hardik Kanak",
    author_email="hardik.kanak@softqubes.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
