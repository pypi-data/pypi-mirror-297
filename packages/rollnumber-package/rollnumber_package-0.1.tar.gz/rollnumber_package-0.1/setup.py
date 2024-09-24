
### 4. **Create `setup.py`**

# Here’s a basic `setup.py` for your package:

# ```python
# setup.py

from setuptools import find_packages, setup

setup(
    name='rollnumber_package',
    version='0.1',
    author='Abhiuday Pratap Singh',
    author_email='abhiuday17@gmail.com',
    description='A simple package to display roll number and name',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://test.pypi.org/project/rollnumber-package/',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
