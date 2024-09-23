from setuptools import setup, find_packages

setup(
    name='canvect',                          
    version='0.1.1',                         
    author='Gnanesh Balusa',                      
    author_email='gnaneshbalusa016g@gmail.com',   
    description='A Python package for CAN bus communication',
    long_description=open('README.md').read(),  
    long_description_content_type='text/markdown',
    url='https://github.com/gnanesh-16/Canvect',  
    packages=find_packages(),                
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',   
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',                 
    install_requires=[                       
        'python-can',
    ],
)
