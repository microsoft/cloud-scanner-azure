from setuptools import setup, find_packages


exec(open('cloud_scanner_azure/version.py').read())
setup(name='cloud_scanner_azure',
      version=__version__,
      description='Core package for scanning Azure cloud resources',
      url='https://microsoft.github.io/cloud-scanner-azure',
      author='Microsoft',
      author_email='cscan@microsoft.com',
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
