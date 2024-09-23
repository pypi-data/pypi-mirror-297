# Processar Imagens com Python (processar-imagem-py)

## Descrição

Módulo Python para processamento e comparação de imagens. Este projeto foi criado durante o Treinamento DIO NTT Data 2024. Ele fornece um conjunto de funções para:

* Carregar e salvar imagens.
* Redimensionar imagens.
* Converter imagens para escala de cinza.
* Calcular a diferença entre duas imagens.
* Equalizar histogramas de imagens.
* Exibir imagens e seus histogramas.

## Instalação

Utilize o gerenciador de pacotes [pip](https://pip.pypa.io/en/stable/) para instalar o `processar-imagem-py`:

```bash
pip install processar-imagem-py

```

## Utilização

```python
# Importe os módulos desejados
from processar_imagem_py import processing, transformation, utils  


# Exemplo de uso das funções:

imagem = utils.io.read_image("caminho/da/imagem.jpg")
imagem_redimensionada = transformation.resize_image(imagem, proportion=0.5)
utils.plot.plot_image(imagem_redimensionada) 
```

## Exemplos

- **Comparar duas imagens e destacar as diferenças:**

```python
from processar_imagem_py import processing, utils

imagem1 = utils.io.read_image("image1.jpg")
imagem2 = utils.io.read_image("image2.jpg")
diferenca = processing.find_difference(imagem1, imagem2)
utils.plot.plot_result(imagem1, imagem2, diferenca)
```
- **Redimensionar uma imagem:**

```python
from processar_imagem_py import transformation, utils

imagem = utils.io.read_image("image.jpg")
imagem_pequena = transformation.resize_image(imagem, 0.5)
utils.plot.plot_image(imagem_pequena)

```

## Estrutura do Projeto


image-processing-package/
├── .gitignore
├── README.md
├── requirements.txt
├── setup.py
└── image_processing
    ├── __init__.py
    ├── processing
    │   ├── __init__.py
    │   ├── combination.py
    │   └── transformation.py
    └── utils
        ├── __init__.py
        ├── io.py
        └── plot.py




## Autor
[Gleyson Atanazio](https://github.com/atnzpe) 

## License
[MIT](https://choosealicense.com/licenses/mit/)





