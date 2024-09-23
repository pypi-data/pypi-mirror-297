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

    name = 'Notification_List',
    version= '0.0.1',
    author= 'Ranjeet Aloriya',
    author_email= 'ranjeet.aloriya@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements("requirements.txt")
    
)