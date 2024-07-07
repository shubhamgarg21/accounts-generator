from setuptools import setup, find_packages

setup(
    name='generate-email',
    version='0.1.1',
    author='Shubham Garg',
    author_email='shubham.garg21@outlook.com',
    packages=find_packages(),
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