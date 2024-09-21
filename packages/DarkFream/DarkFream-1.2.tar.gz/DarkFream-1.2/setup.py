from setuptools import setup

setup(
    name='DarkFream',
    version='1.2',  # Update the version number to 1.2
    author='vsp210',
    author_email='vsp210@gmail.com',
    description='My Python library',
    packages=['DarkFream'],
    entry_points={
        'console_scripts': [
            'dark=DarkFream.main:main',
        ],
     },
    install_requires=['winotify>=1.1.0', 'Jinja2>=3.1.4', 'MarkupSafe>=2.1.5'],
)
