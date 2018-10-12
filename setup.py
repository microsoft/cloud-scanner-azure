from setuptools import setup, find_packages

setup(name='cloud_scanner_azure',
      version='0.1',
      description='Core package for scanning Azure cloud resources',
      url='',
      author='Tanner Barlow',
      author_email='tanner.barlow12@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'azure-mgmt-nspkg',
          'azure-mgmt-resource',
          'azure-mgmt-subscription',
          'azure-servicebus',
          'azure-storage',
          'azure-storage-common',
          'azure-cosmosdb-table',
          'azure-functions'
      ])
