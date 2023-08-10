from setuptools import setup

setup(
    name='Next Frontier Project',
    version='0.1.11',
    description='Personal Assistant Project',
    license='MIT',
    author='Next Frontier',
    packages=['personal_assistant'],
    install_requires=['rich'],
    entry_points={
        'console_scripts': [
            'personal_assistant = personal_assistant.main_menu:menu'
        ]
    }
)