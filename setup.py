import setuptools

# Reads the content of your README.md into a variable to be used in the setup below
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='wifi_wrapper',                           
    packages=['wifi_wrapper'],                     
    version='0.1.0',                               
    license='MIT',                                 
    description='A python wrapper over nmcli tool for linux devices.',
    long_description=long_description,              
    long_description_content_type="text/markdown",  
    author='Hrithik Yadav',
    author_email='hrithiky328@gmail.com',
    url='https://github.com/hrithik098/wifi_wrapper', 
    project_urls = {                                
        "Bug Tracker": "https://github.com/hrithik098/wifi_wrapper/issues"
    },
    install_requires=[],                  
    keywords=["pypi", "nmcli", "wifi tools"],
    classifiers=[  
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
    ],
    
    download_url="https://github.com/hrithik098/wifi_wrapper/archive/refs/tags/0.1.0.tar.gz",
)