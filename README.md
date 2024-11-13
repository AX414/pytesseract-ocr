# Reconhecimento óptico de caracteres com pytesseract
Um código em Python desenvolvido para ler diversas imagens contendo nomes e números de contatos (tipo a lista do whatsapp), feito justamente para você gerar essa lista como texto para auxiliar em alguma automatização, por exemplo.

É necessário instalar a biblioteca pandas e pytesseract pelo pip com ``` pip install pandas ``` e ``` pip install pytesseract ``` e se estiver no windows, instale ele no seu computador, utilize o link <a href="https://github.com/tesseract-ocr/tesseract/releases/download/5.5.0/tesseract-ocr-w64-setup-5.5.0.20241111.exe">aqui</a> e instale o .exe do tesseract, depois insira ele no PATH do seu sistema.

## Como funciona?

Após executar o projeto, o programa irá utilizar as bibliotecas do pytesseract para realizar o reconhecimento óptico dos caracteres e armazenará eles em uma lista temporária, que será utilizada para gerar um dataframe pela biblioteca pandas e irá apresentar pelo próprio terminal, além disso, também é possível ver  o resultado será um dataframe pela biblioteca pandas em seu terminal. Junto deste projeto também é possível ver duas imagens de exemplo:

![Imagem de Teste 1](https://github.com/AX414/pytesseract-ocr/blob/main/imgs/1.jpg)
![Imagem de Teste 2](https://github.com/AX414/pytesseract-ocr/blob/main/imgs/2.jpg)

Elas foram feitas pelo documento de notas então é óbvio que será algo fácil de visualizar, então em documentos com a coloração mais escura ou muito clara, é possível que você tenha de alterar a escala de cores para deixar o contraste da imagem mais escuro ou mais claro, dependendo do caso.

Após executar o programa, a saída será semelhante à essa:

![Imagem do dataframe](https://github.com/AX414/pytesseract-ocr/blob/main/screenshots/1.jpg)

E também é realizado um documento .json para qualquer outra necessidade futura:

![Imagem do Json](https://github.com/AX414/pytesseract-ocr/blob/main/screenshots/2.jpg)
