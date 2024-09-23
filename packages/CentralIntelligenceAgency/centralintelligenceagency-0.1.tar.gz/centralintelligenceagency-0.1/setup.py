from setuptools import setup, find_packages

setup(
    name='CentralIntelligenceAgency',  # Neuer, eindeutiger Name
    version='0.1',
    packages=find_packages(),
    install_requires=[
        # Abhängigkeiten hier hinzufügen
    ],
    entry_points={
        'console_scripts': [
            'ciaapp=mein_paket.main:main_function',  # Konsolenbefehl
        ],
    },
    description='Paket der Central Intelligence Agency',
    author='staatsberater',
    author_email='staatsberater@instagram.com',
    url='https://github.com/dukeskardashian',
)
