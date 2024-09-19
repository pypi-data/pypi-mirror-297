from setuptools import setup

setup(
    name='myHttp',
    version='1.2.0',
    author='Tiancheng Jiao',
    author_email='jtc1246@outlook.com',
    url='https://github.com/jtc1246/myHttp',
    description='A very easy http tool',
    packages=['myHttp'],
    install_requires=['urllib3<2'],
    python_requires='>=3',
    platforms=["all"],
    license='GPL-2.0 License'
)

