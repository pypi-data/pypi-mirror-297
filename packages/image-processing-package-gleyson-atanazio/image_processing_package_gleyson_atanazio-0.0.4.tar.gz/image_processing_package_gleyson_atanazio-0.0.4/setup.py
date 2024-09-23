# Importa as funções necessárias do módulo setuptools.
# - setup:  Função principal para configurar o pacote.
# - find_packages:  Função para encontrar automaticamente os pacotes dentro do projeto.
from setuptools import setup, find_packages

# Abre o arquivo README.md em modo de leitura ("r").
# (Explícito é melhor que implícito: o código deixa claro que o arquivo será aberto para leitura).
with open("README.md", "r", encoding="utf-8") as f:
    # Lê o conteúdo do arquivo README.md e armazena na variável page_description.
    # (Atribuição simples: o código atribui o conteúdo do arquivo a uma variável de forma direta).
    page_description = f.read()

# Abre o arquivo requirements.txt em modo de leitura ("r").
# (Reaproveitamento de código: o código usa a mesma estrutura with open para abrir outro arquivo).
with open("requirements.txt") as f:
    # Lê o conteúdo do arquivo, divide as linhas em uma lista e armazena na variável requirements.
    requirements = f.read().splitlines()

# Chama a função setup para configurar o pacote.
# (Um único lugar para configurações: todas as informações relevantes do pacote estão neste bloco).
setup(
    name="image_processing-package-gleyson-atanazio",  # Nome do pacote (deve ser único no PyPI).
    version="0.0.4",  # Versão do pacote (seguir o versionamento semântico).
    author="Gleyson Atanazio",  # Nome do autor.
    author_email="gleysonasilva@gmail.com",  # Email do autor.
    description="Módulo para processamento e comparação de imagens.",  # Descrição curta do pacote.
    long_description=page_description,  # Descrição longa do pacote (geralmente o conteúdo do README.md).
    long_description_content_type="text/markdown",  # Define o formato da descrição longa como Markdown.
    url="https://github.com/atnzpe/processar-imagem-py",  # URL do repositório do projeto.
    packages=find_packages(),  # Encontra e inclui automaticamente os pacotes do projeto.
    install_requires=requirements,  # Define as dependências do pacote (a partir do requirements.txt).
    python_requires=">=3.8",  # Define a versão mínima do Python necessária para o pacote.
)
