from setuptools import setup, find_packages
import os


def read_file(filename):
    with open(os.path.join(os.path.dirname(__file__), filename), encoding='utf-8') as f:
        return f.read()

setup(
    name='vendas_analise',
    version='0.0.1',
    packages=find_packages(),
    description='Um pacote para análise de vendas',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    author='Luiz Vaz',
    author_email="luiz.henrique.vaz@hotmail.com",
    url='https://github.com/luiz-vaz/vendas_analise_package'  # Altere para a URL do seu repositório
)