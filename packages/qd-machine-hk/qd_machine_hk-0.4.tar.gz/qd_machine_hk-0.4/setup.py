# setup.py

from setuptools import setup,find_packages, Extension
from Cython.Build import cythonize

# Define the extension module
extensions = [
    Extension("qd_machine_hk.ParentMachineInterface", ["qd_machine_hk/ParentMachineInterface.pyx"])
]

# Setup function for building the module
setup(
    name="qd_machine_hk",
    version='0.4',
    author="Hardik Kanak",
    author_email="hardik.kanak@softqubes.com",
    description="Machine package",
    packages=find_packages(),

    install_requires=[
        'requests==2.31.0',
        'psutil==6.0.0',
        'GPUtil==1.4.0',
        'Cython==3.0.11'
    ],

    # Include Cython extensions
    ext_modules=cythonize(extensions)
)

