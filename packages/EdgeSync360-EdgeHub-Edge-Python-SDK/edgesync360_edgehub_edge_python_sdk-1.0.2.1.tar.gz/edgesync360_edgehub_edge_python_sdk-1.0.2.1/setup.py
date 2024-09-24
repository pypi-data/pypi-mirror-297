import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="EdgeSync360_EdgeHub_Edge_Python_SDK",
    version="1.0.2.1",
    author="Paul Tseng",
    author_email="edgehub.dev@gmail.com",
    description="EdgeSync360_EdgeHub_Edge_Python_SDK package allows developers to write Python applications which access the EdgeSync360/EdgeHub Platform via MQTT protocol.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/EdgeHub-Repo/dc-edge-sdk-python-sample",
    packages=setuptools.find_packages(),
    install_requires=[
        "paho-mqtt==1.6.1",
        "azure-iot-device",  # Add other dependencies as needed
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)
