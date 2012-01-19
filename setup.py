from setuptools import setup


version = '0.0.0beta'
long_description = '\n\n'.join([open('README.rst').read()])

setup(name='monologue',
      version=version,
      description="Monologue - A cool logging module !",
      long_description=long_description,
      classifiers=[],
      keywords='logging',
      author='Feth',
      author_email='feth@tuttu.info',
      packages=['monologue'],
      namespace_packages=[],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ]
      )
