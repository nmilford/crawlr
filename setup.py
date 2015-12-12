from setuptools import setup

setup(name='crawlr',
      version='0.1',
      description='A Toy Crawler',
      url='http://github.com/nmilford/crawlr',
      author='Flying Circus',
      author_email='nathan@milford.io',
      license='ASL',
      packages=['crawlr'],
      install_requires=[
        'tld',
        'requests',
        'beautifulsoup4'
      ]
      zip_safe=False)


