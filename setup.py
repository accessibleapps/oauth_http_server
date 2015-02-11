from setuptools import setup, find_packages

__doc__ = """A simple http server for parsing oauth callbacks for desktop apps pretending to be webapps"""

setup(
 name = 'oauth_http_server',
 version = 0.1,
 description = __doc__,
 py_modules = ['oauth_http_server'],
 classifiers = [
  'Development Status :: 4 - Beta',
  'Intended Audience :: Developers',
  'Programming Language :: Python',
  'Topic :: Software Development :: Libraries',
 ],
)
