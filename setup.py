from distutils.core import setup
setup(
  name='NetworkController',
  packages=['NetworkController'], # this must be the same as the name above
  version='0.1',
  description='Python Wrapper for clumsy network tool. For simulating network issues in your automation tests. '
                'Examine your product with unstable network. Easy to use.',
  author='Doron Friedlander',
  author_email='doron0123@gmail.com',
  url='https://github.com/DoronFried/ClumsyWrapper', # use the URL to the github repo
  download_url = 'https://github.com/DoronFried/ClumsyWrapper/tarball/0.1', # link to the tar zip file of the package
  keywords = ['network', 'clumsy', 'testing', 'automation tests'], # arbitrary keywords
  classifiers = [],
)

