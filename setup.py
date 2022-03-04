from glob import glob
from os.path import basename
from os.path import splitext
from setuptools import setup, find_packages


install_requires = [
    "matplotlib",
    "qulacs", 
    "qiskit_terra", 
    "amazon-braket-sdk", # 必要な依存ライブラリがあれば記述
    "pytest"
]

packages=find_packages()

extras_require={
    "qlib":["qulacs", "qiskit", "amazon-braket-sdk"]
}

quantum_packages = ['qulacs', 'qiskit', 'braket']

setup(
    name='naniwa',
    version='0.0.1',
    description='This is a library of converting qulacs circuits to an quantum circuit on another library.',
    packages=packages,
    install_requires=install_requires,
)
