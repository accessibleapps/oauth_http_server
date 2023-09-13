from setuptools import setup, find_packages
import io
__doc__ = """A simple http server for parsing oauth callbacks for desktop apps pretending to be webapps"""
readme = io.open('README.rst', encoding='utf-8').read()
setup(
    name='oauth_http_server',
    version='1.1.0',
    description=__doc__,
    long_description=readme,
    py_modules=['oauth_http_server'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
    ],
)
