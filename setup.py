from setuptools import setup


setup(name='bdl.engines.eightchan',
      version='1.0.0',
      description='8ch.net engine for BDL',
      url='https://www.github.com/Wawachoo/BDL_8CH',
      author='Wawachoo',
      author_email='Wawachoo@users.noreply.github.com',
      license='GPLv3',
      classifiers = ['Development Status :: 3 - Alpha',
                     'Environment :: Console',
                     'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                     'Natural Language :: English',
                     'Operating System :: OS Independent',
                     'Programming Language :: Python :: 3 :: Only',
                     'Communications :: File Sharing',
                     'Topic :: Internet'],
      keywords='8CH download',
      packages=['bdl.engines.eightchan', ],
      entry_points = {'bdl.engines': ['module=bdl.engines.eightchan']},
      install_requires=['lxml', 'requests'],
      package_data={"bdl.engines.eightchan": ["sites.json", ]})
