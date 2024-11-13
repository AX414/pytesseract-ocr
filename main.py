import pytesseract
import re
import os
import json
import pandas as pd
from PIL import Image, ImageOps, ImageEnhance

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
diretorio_imagens = 'imgs'
contatos_extraidos = []

def limpar_telefone(telefone):
    telefone = re.sub(r'[^\d+]', '', telefone)
    if telefone.startswith("+55"):
        telefone = telefone[:3] + " " + telefone[3:5] + " " + telefone[5:10] + "-" + telefone[10:]
    elif telefone.startswith("55"): # Caso faltar o +
        telefone = "+" + telefone[:2] + " " + telefone[2:4] + " " + telefone[4:9] + "-" + telefone[9:]
    else: # Caso não tenha sequer o número que indique o país
        telefone = telefone[:2] + " " + telefone[2:7] + "-" + telefone[7:]
    return telefone

def limpar_nome(nome):
    nome = re.sub(r'[^\w\s]', '', nome)
    return nome

def processar_imagem(imagem_path):
    contatos_imagem = []
    imagem = Image.open(imagem_path)
    imagem = ImageOps.exif_transpose(imagem)
    enhancer = ImageEnhance.Contrast(imagem)
    imagem = enhancer.enhance(2.0)
    imagem = imagem.convert("L")
    texto_extraido = pytesseract.image_to_string(imagem)
    linhas = texto_extraido.splitlines()
    telefone_regex = re.compile(r'\+?\d[\d\s-]*')
    nome = None
    telefone = None

    for linha in linhas:
        linha = linha.strip()
        if not linha or re.search(r'[^\x00-\x7F]+', linha):
            continue
        if telefone_regex.match(linha):
            if len(linha.replace(" ", "").replace("-", "")) >= 10:
                telefone = limpar_telefone(linha)
            else:
                telefone = None
        else:
            nome = limpar_nome(linha)
        if nome and telefone:
            contatos_imagem.append({'Nome': nome, 'Telefone': telefone})
            nome = None
            telefone = None

    return contatos_imagem

def processar_todas_imagens():
    arquivos_imagem = [f for f in os.listdir(diretorio_imagens) if f.endswith('.jpg')]
    for arquivo in arquivos_imagem:
        imagem_path = os.path.join(diretorio_imagens, arquivo)
        contatos = processar_imagem(imagem_path)
        contatos_extraidos.extend(contatos)

processar_todas_imagens()

if contatos_extraidos:
    # Salvando os contatos em um arquivo JSON
    with open('contatos_extraidos.json', 'w', encoding='utf-8') as f:
        json.dump(contatos_extraidos, f, ensure_ascii=False, indent=4)
    print("Contatos extraídos e salvos em 'contatos_extraidos.json'.")

    # Exibindo os contatos como uma tabela usando pandas
    df = pd.DataFrame(contatos_extraidos)
    print("\nTabela de Contatos Extraídos:")
    print(df.to_markdown())  # Exibindo como tabela com formatação de markdown para ficar bonitinho

else:
    print("Nenhum contato foi extraído.")
