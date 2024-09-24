from setuptools import setup, find_packages  

setup(  
    name='my_binary_package',  
    version='0.1',  
    packages=find_packages(),  
    description='A simple example package with binary distributions',  
    author='Your Name',  
    author_email='your.email@example.com',  
    url='https://github.com/yourusername/my_binary_package',  
    classifiers=[  
        'Programming Language :: Python :: 3',  
        'License :: OSI Approved :: MIT License',  
        'Operating System :: OS Independent',  
    ],  
    python_requires='>=3.6',  
)