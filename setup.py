from glob import glob
from os.path import basename
from os.path import splitext
from setuptools import setup, find_packages


install_requires = [
    "matplotlib",
    "qulacs", 
    "qiskit_terra", 
    "amazon-braket-sdk" # 必要な依存ライブラリがあれば記述
]

packages=find_packages()

extras_require={
    "qlib":["qulacs", "qiskit", "amazon-braket-sdk"]
}

py_modules=[splitext(basename(path))[0] for path in glob('converter/*.py')]

setup(
    name='naniwa',
    version='0.0.1',
    description='This is a library of converting qulacs circuits to an quantum circuit on another library.',
    packages=packages,
    install_requires=install_requires,
    py_modules=py_modules,
)