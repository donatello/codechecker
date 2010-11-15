from distutils.core import setup

setup(name='codechecker',
      version='1.0',
      description='Codechecker components',
      long_description='A Python based software to host'
                       'Online Programming Contests',
      author='Suren, Aditya and Krishnan',
      author_email='codechecker@googlecode.com', 
      license='GPLv3',
      url='http://code.google.com/p/codechecker',
      platforms='All',
      packages=['cc_backend', 'cc_backend.compiler', 'cc_backend.evaluator',
                'cc_backend.score', 'cc_backend.se', 'cc_backend.store'],
      package_dir={'cc_backend' : 'cc_backend/src'}
      )


