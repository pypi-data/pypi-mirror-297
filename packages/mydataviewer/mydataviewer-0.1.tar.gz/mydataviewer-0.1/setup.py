from setuptools import setup, find_packages
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()
    
setup(
    name='mydataviewer',
    version='0.1',
    description='A Lightweight Real-Time Interactive Data Viewer for Python',
    author='Mohsen Askar',
    author_email='ceaser198511@gmail.com',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    include_package_data=True,
    package_data={
        'mydataviewer': [
            'assets/icon.ico',
            'docs/images/*.png',
            ],
    },
    install_requires=[
        'pandas',
        'pyqt5',
        'qtconsole',
        'ipykernel',
        'jupyter_client'
    ],
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    url='https://github.com/MohsenAskar',
    entry_points={
        'console_scripts': [
            'viewdata=mydataviewer.view_dataframe:main',
        ],
    },
)