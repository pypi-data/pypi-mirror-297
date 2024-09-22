from setuptools import setup, find_packages

setup(
    name='py_mod_test',
    version='1.0.9',  # Versão inicial, será atualizada automaticamente
    description='Ferramenta para deploy de pacotes Python',
    long_description=open('README.md').read(),  # Adicione um README.md para descrição longa
    long_description_content_type='text/markdown',
    author='Fernando Pessoa',
    author_email='fefe@example.com',  # Adicione seu email aqui
    url='https://github.com/fpessoa64/py_mod_test',
    packages=find_packages(),
    install_requires=[],  # Adicione dependências aqui se houver
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Mude se usar outra licença
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Especifica a versão mínima do Python

)