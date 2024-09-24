from setuptools import setup, find_packages

setup(
    name='browser_manager',
    version='0.2.0',  # Atualize conforme necessário
    author='Dux Tecnologia',
    author_email='contato@tpereira.com.br',
    description='A library for browser automation and management.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/duxtec/browser_manager',  # Atualize com o URL do seu repositório
    packages=find_packages(),
    install_requires=[
        'selenium',
        'webdriver-manager',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Altere conforme necessário
)
