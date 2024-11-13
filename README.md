# Reconhecimento óptico de caracteres com pytesseract
Um código em Python desenvolvido para ler uma imagem contendo nomes e números de contatos (tipo a lista do whatsapp), feito justamente para você gerar essa lista como texto para auxiliar em alguma automatização, por exemplo.

É necessário instalar o pytesseract pelo pip com ``` pip install pytesseract ``` e se estiver no windows, instalar ele, utilize o link <a href="https://github.com/tesseract-ocr/tesseract/releases/download/5.5.0/tesseract-ocr-w64-setup-5.5.0.20241111.exe">aqui</a> e instale o .exe do tesseract, depois insira ele no PATH do sistema.

Após executar o projeto, o resultado será um dataframe pela biblioteca pandas em seu terminal:

![Imagem do dataframe](https://github.com/AX414/pytesseract-ocr/blob/main/screenshots/1.jpg)

E também é realizado um documento .json para qualquer outra necessidade futura:

![Imagem do Json](https://github.com/AX414/pytesseract-ocr/blob/main/screenshots/2.jpg)
