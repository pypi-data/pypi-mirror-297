from setuptools import setup, find_packages


setup(
    name='griffin-vision',
    version='0.0.0',
    packages=find_packages(),
    install_requires=[
        # List your dependencies here
        "qdrant-client==1.11.1",
        "transformers==4.44.2",
        "requests==2.32.3",
        "torch==2.4.1"
    ],
    description='A package for performing text-to-image and image-to-image searches using embedding-based techniques',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='JunaidBashir',
    author_email='junaidkernel@gmail.com',
    url='https://github.com/junaidbashir11/griffin',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
