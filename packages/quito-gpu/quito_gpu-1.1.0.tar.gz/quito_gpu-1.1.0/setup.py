import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="quito-gpu",
    version="1.1.0",
    author="Xinyi Wang",
    author_email="xinyi@simula.no",
    description="A coverage guided test generator for quantum programs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    url="https://github.com/Simula-COMPLEX/quito",
    classifiers= ["Programming Language :: Python :: 3",  # 编程语言
        "License :: OSI Approved :: MIT License",  # license
        "Operating System :: OS Independent"],  # 操作系统
    install_requires=[
        "qiskit==1.2.1",
        "qiskit-aer-gpu==0.15.1"
    ],
    package_data={"pipmodule": ["*.png"]},
    python_requires=">=3.8",
    entry_points={
        'console_scripts': [
            'quito = quito:help'
 ]
    }
)