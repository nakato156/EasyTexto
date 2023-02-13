from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    readme = f.read()

setup(
    name='EasyTexto',
    version='0.4',
    license='MIT',
    description='Paquete para manejar archivos de texto de forma sencilla',
    long_description_content_type="text/markdown",
    long_description=readme,
    author='Christian (Nakato)',
    author_email='christianvelasces@gmail.com',
    url='https://github.com/nakato156/EasyTexto',
    keywords=['file', 'files', 'text'],
    packages=find_packages(),
)