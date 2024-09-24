from setuptools import setup, find_packages
from typing import List

trigger_mode = "-e ."

def get_requirements(file_path: str) -> List[str]:
    requirements = []
    with open(file_path) as f:
        requirements = f.readlines()
        requirements = [r.replace("\n", "") for r in requirements]
        if trigger_mode in requirements:
            requirements.remove(trigger_mode)

    return requirements


setup(

    name = 'NotificationList',
    version= '0.0.3',
    author= 'Ranjeet Aloriya',
    author_email= 'ranjeet.aloriya@gmail.com',
    description='A Python package for consolidating breach response notification lists efficiently.',
    long_description="""
        The Breach Response Notification List package is designed to streamline the process of consolidating 
        notification lists for affected parties based on unique identifiers. This package addresses the challenges 
        of generating accurate notifications while handling variations in names and ensuring no affected parties 
        are notified twice. With this tool, you can reduce the time spent on creating notification lists from 
        weeks to under a minute, even for large datasets. It generates a merging ID for all unique parties, 
        making the notification process efficient and reliable.
    """,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Natural Language :: English',
        'Environment :: Console',
    ],
    python_requires='>=3.6',
    install_requires=get_requirements("requirements.txt"),
    include_package_data=True,
    keywords='breach response, notification lists, data consolidation, unique identifiers, affected parties, data merging, efficiency tools, duplicate notifications'
    
)