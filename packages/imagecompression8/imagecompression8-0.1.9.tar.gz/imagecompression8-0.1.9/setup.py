from setuptools import setup, find_packages

setup(
    name='imagecompression8',
    version='0.1.9',
    packages=find_packages(),
    description='It is an image compression Python package based on Singular Value Decomposition (SVD) technology. This tool offers an efficient block-based image compression method, reducing the storage requirements of images by dividing them into blocks and applying SVD, while retaining as much visual information as possible.',
    install_requires=[
        'numpy',
        'pillow',
        'scipy',
    ],
    author='Katie Wen-Ling Kuo',
    author_email='katie20030705@gmail.com',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
    python_requires='>=3.6',
)