from setuptools import setup

import product_details


setup(
    name='django-mozilla-product-details',
    version=product_details.__version__,
    description='Product and locale details for Mozilla products.',
    long_description=open('README.md').read(),
    author='Fred Wenzel',
    author_email='fwenzel@mozilla.com',
    url='http://github.com/fwenzel/django-mozilla-product-details',
    license='BSD',
    packages=['product_details'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['Django>=1.1'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Environment :: Web Environment :: Mozilla',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
