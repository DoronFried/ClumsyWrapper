from distutils.core import setup
setup(
  name='ClumsyWrapper',
  packages=['ClumsyWrapper', 'ClumsyWrapper/TestsExample'],
  version='0.2',
  description='Python Wrapper for clumsy network tool. For simulating network issues in your automation tests. '
                'Examine your product with unstable network. Easy to use.',
  author='Doron Friedlander',
  author_email='doron0123@gmail.com',
  url='https://github.com/DoronFried/ClumsyWrapper', # use the URL to the github repo
  download_url = 'https://github.com/DoronFried/ClumsyWrapper/tarball/v0.1-alpha', # link to the tar zip file of the package
  keywords = ['network', 'clumsy', 'testing', 'automation tests'], # arbitrary keywords
  classifiers = [],
)

