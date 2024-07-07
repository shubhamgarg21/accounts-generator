from setuptools import setup, find_packages

setup(
    name='generate-email',
    version='0.1.0',
    author='Shubham Garg',
    author_email='shubham.garg21@outlook.com',
    license='GPLv3',
    packages=find_packages(),
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'selenium',
        'playwright',
        'requests',
        'selenium-stealth',
        'random-password-generator',
        'Faker',
        'lxml',
        'fake-headers',
        'pillow',
    ],
    # entry_points={
    #     'console_scripts': [
    #         'generate-email=generate_email.run:main',
    #     ],
    # },
)