# Image Processor

Um pacote simples de processamento de imagens. 

## Funcionalidades
- Converter imagens para tons de cinza.
- Redimensionar imagens.

## Instalação

```bash
pip install image_processor

```

## Uso

```python
from image_processor import convert_to_grayscale, resize_image

# Converter uma imagem para tons de cinza
convert_to_grayscale('imagem.jpg', 'saida.jpg')

# Redimensionar uma imagem
resize_image('imagem.jpg', 'saida_redimensionada.jpg', (200, 200))


Agora o arquivo `README.md` tem uma explicação para qualquer pessoa que for usar o seu pacote, incluindo o exemplo de código que você também pode usar para testar.

---

### Como Testar no VS Code

Agora, para **testar** as funções do seu pacote, siga os passos abaixo no terminal do VS Code.

#### 1. **Instalar o Pacote Localmente**

Para garantir que tudo está funcionando corretamente, você precisa "instalar" o seu pacote localmente, como se fosse um pacote vindo do PyPI.

No terminal do VS Code, estando na pasta raiz do seu projeto (onde está o arquivo `setup.py`), execute o comando:

```bash
pip install .

