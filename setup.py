from setuptools import setup, find_packages

setup(
    name='upperlimbs',
    version='0.1.0',
    author='Suman Shrestha',
    author_email='sthasmn@gmail.com',
    description='A Python package to measure and visualize upper limb movements using MediaPipe.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='http://github.com/sthasmn/UpperLimbs',
    packages=find_packages(),
    install_requires=[
        'opencv-python',
        'mediapipe',
        'numpy',
        'matplotlib',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)