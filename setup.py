from setuptools import setup

setup(name='spicemodels',
    version='2.1',
    description='Convert between .OBJ and .BDS (DSK) files',
    author='Alfredo Escalante',
    author_email='alfredoescalante95@gmail.com',
    # license='GPL',
    packages=['spicemodels'],
    install_requires=['numpy'],
    python_requires='>=3',
)