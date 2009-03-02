from setuptools import setup, find_packages

setup(
    name='django-email-usernames',
    version='0.1.0',
    description='Use email addresses as username for Django non-staff users.',
    author='Hakan Waara',
    author_email='hwaara@gmail.com',
    url='http://bitbucket.org/hakanw/django-email-usernames/',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ]
)