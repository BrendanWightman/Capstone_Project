from setuptools import find_packages, setup

# To use
# pip install -e .

setup(
    name='Telingo',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask', 
        'flask_sqlalchemy',
        'python-dotenv',
        'password_validation',
        'requests',
        'flask_socketio'
    ],
)