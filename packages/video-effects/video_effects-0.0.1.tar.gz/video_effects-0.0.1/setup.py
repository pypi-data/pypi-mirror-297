from setuptools import setup, find_packages

setup(
    name='video-effects',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'moviepy',
        'numpy',
        'opencv-python',
        'pillow'
    ],
    description='A package for video effects',
    author='0xIbra',
    author_email='ibragim.ai95@gmail.com',
    url='https://github.com/yourusername/video-effects',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
