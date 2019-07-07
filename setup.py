from setuptools import setup, find_packages

version = '0.1.5'
#'SomePackage>=1.0.4'
install_requires = [
    'SQLAlchemy>=0.7.9',
    'winpaths>=0.1',
    'pywin32>=224',
    'numpy>=1.16.0',
    'ast>=0.0.2'
    ]

setup(
    name             = 'xelmemo',
    version          = version,
    description      = 'python library for xelmemo',
    license          = 'MIT',
    author           = 'montrix',
    author_email     = 'master@montrix.co.kr',
    url              = 'http://www.montrix.co.kr/xelmemo',
    download_url     = 'http://www.montrix.co.kr/xelmemo/download/xelmemo_' + version + '.tar.gz',
    install_requires = install_requires,
    packages         = find_packages(exclude = ['test']),
    keywords         = ['excel', 'finance', 'xelmemo'],
    # python_requires  = '>=2.7',
    package_data     =  { },
    zip_safe=False,
    classifiers      = [
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3'
    ]
)