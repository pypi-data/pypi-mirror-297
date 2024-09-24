from setuptools import setup

setup(name='aifactory',
      version='2.0.0',
      description='aifactory-cli',
      author='aifactory',
      author_email='contact@aifactory.page',
      url='https://aifactory.space',
      license='MIT',
      py_modules=['submit'],
      python_requires='>=3',
      install_requires=["pipreqs", "ipynbname", "gdown", "requests", "IPython"],
      packages=['aifactory']
      )
