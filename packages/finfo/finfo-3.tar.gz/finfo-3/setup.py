from setuptools import setup, find_packages

setup(
  name = 'finfo',
  version = '3', 
  packages = find_packages(),
  description = 'Package used to find fencers ranking placements.', 
  long_description=open('README.md').read(),
  long_description_content_type='text/markdown',
  author = 'Hannibal Lykke Kofoed',
  author_email = 'hanniballykkekofoed@icloud.com', 
  # It is possible to add entrypoints.
  install_requires=[
        'pypdf',
        'requests'
  ],
  license='MIT',
  url = 'https://gitlab.com/hann1ba1/finfo',
  keywords = ['python', 'fencing', 'rankings'],
   classifiers=[
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',
    'Operating System :: OS Independent',
  ]
)

# pip install setuptools wheel twine
# python setup.py sdist bdist_wheel

# twine upload dist/* -u __token__ -p pypi-AgEIcHlwaS5vcmcCJGNmZjRmZWQ0LTg4MWUtNGE2NS1hYzQ5LTkzNDJhNjcwYTFjMwACKlszLCI1ZTY2YTYyYy03NGQxLTQxMjAtYTg3MC0xMDJiMWMzZjRkOGYiXQAABiAt8kZFSbYQBjaWcKyKiBGCjzU06D1KcD0aunzIwS-Low

