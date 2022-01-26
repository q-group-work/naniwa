from glob import glob
from os.path import basename
from os.path import splitext
from setuptools import setup, find_packages


install_requires = [
    "matplotlib" # 必要な依存ライブラリがあれば記述
]

packages=find_packages()
# packages=['converter.qulacs']

package_dir={'naniwa':'converter'}

scripts = ['converter/qulacs/qulacs_converter.py']

console_scripts = [
    # 'naniwa = converter.converter:convert',
]

extras_require={
    "qlib":["qulacs", "qiskit"]
}

py_modules=[splitext(basename(path))[0] for path in glob('converter/*.py')]

setup(
    name='naniwa',
    version='0.0.1',
    description='This is a library of converting qulacs circuits to an quantum circuit on another library.',
    packages=packages,
    package_dir=package_dir,
    # scripts=scripts,
    install_requires=install_requires,
    extras_require=extras_require,
    # entry_points={'console_scripts': console_scripts},
    py_modules=py_modules,
)