import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="toytool",
    version="0.0.1",
    author="HandsomeBoy",
    author_email="putaoisapig@163.com",
    description="toy-tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=["pillow", "opencv-python", "opencv-python-headless"]
)