from setuptools import setup, find_packages

setup(
    name='give-me-the-odds',
    version='0.3',
    packages=find_packages(),
    install_requires=[
        'click',
    ],
    entry_points='''
      [console_scripts]
      give_me_the_odds=cli.give_me_the_odds:give_me_the_odds
      ''',
)
