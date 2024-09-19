from setuptools import setup, find_packages

setup(
    name='pipnet',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'torch',
        'torchvision',
        'opencv-python==4.10.0.84',
        'numpy==1.24.3',
        'Pillow==10.4.0',
    ],
    description='A package for PIPNet - landmark prediction using ResNet and MobileNet models',
    author='Dat Viet Thanh Nguyen',
    author_email='thanhdatnv2712@gmail.com',
    url='https://github.com/datvtn/PIPNet',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
