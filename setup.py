from setuptools import setup

setup(name='monique_worker_py',
      version='0.1.0.0',
      description='Python wrapper to Monique system',
      url='https://github.com/biocad/monique-worker-py',
      author='Bogdan Neterebskii',
      author_email='neterebskiy@biocad.ru',
      license='BSD3',
      packages=['monique_worker_py'],
      zip_safe=False,
      install_requires=['pyzmq'])
