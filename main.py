import pytesseract
from PIL import Image, ImageOps, ImageEnhance
import re
import os
import json  # Importação para trabalhar com JSON

# Defina o caminho da instalação do Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Diretório das imagens
diretorio_imagens = 'imgs'

# Lista para armazenar todos os contatos extraídos
contatos_extraidos = []

# Função para limpar o número de telefone e formatar corretamente
def limpar_telefone(telefone):
    # Remove os parênteses e espaços se existirem
    telefone = re.sub(r'[^\d+]', '', telefone)

    # Verifica se o número começa com o código do país (+55)
    if telefone.startswith("+55"):
        # Se já tiver o +55, apenas formatamos
        telefone = telefone[:3] + " " + telefone[3:5] + " " + telefone[5:10] + "-" + telefone[10:]
    elif telefone.startswith("55"):
        # Se começar com 55 sem o "+", colocamos o "+" na frente
        telefone = "+" + telefone[:2] + " " + telefone[2:4] + " " + telefone[4:9] + "-" + telefone[9:]
    else:
        # Caso não tenha o código de país, deixamos o número como está
        telefone = telefone[:2] + " " + telefone[2:7] + "-" + telefone[7:]

    return telefone

# Função para limpar o nome de clientes
def limpar_nome(nome):
    # Remove caracteres indesejados, como pontos, underscores, etc.
    nome = re.sub(r'[^\w\s]', '', nome)  # Remove caracteres não alfanuméricos e não espaços
    return nome

# Função para processar uma imagem individual e extrair contatos
def processar_imagem(imagem_path):
    # Lista para armazenar os contatos extraídos da imagem atual
    contatos_imagem = []

    # Carrega a imagem original
    imagem = Image.open(imagem_path)

    # Ajuste para corrigir a rotação (detectando a orientação da imagem)
    imagem = ImageOps.exif_transpose(imagem)  # Tenta corrigir a rotação de acordo com os metadados EXIF

    # Aumenta o contraste da imagem para melhorar a precisão do OCR
    enhancer = ImageEnhance.Contrast(imagem)
    imagem = enhancer.enhance(2.0)  # Aumenta o contraste em 2 vezes, ajuste se necessário

    # Converte para escala de cinza para melhorar a clareza
    imagem = imagem.convert("L")

    # Extrai o texto da imagem
    texto_extraido = pytesseract.image_to_string(imagem)

    # Divide o texto extraído em linhas
    linhas = texto_extraido.splitlines()

    # Expressão regular para detectar números de telefone no formato internacional
    telefone_regex = re.compile(r'\+?\d[\d\s-]*')

    # Variáveis temporárias para armazenar nome e telefone enquanto percorremos as linhas
    nome = None
    telefone = None

    # Loop para processar cada linha individualmente
    for linha in linhas:
        linha = linha.strip()

        # Ignora linhas vazias e entradas não válidas
        if not linha or re.search(r'[^\x00-\x7F]+', linha):  # Remover caracteres especiais não alfabéticos
            continue

        # Se a linha parece um número de telefone
        if telefone_regex.match(linha):
            # Validação mais estrita do telefone
            if len(linha.replace(" ", "").replace("-", "")) >= 10:  # Espera-se um número com pelo menos 10 dígitos
                telefone = limpar_telefone(linha)  # Limpa o telefone removendo caracteres indesejados e formata
            else:
                telefone = None  # Se o telefone não for válido, ignoramos
        else:
            # Se não for um telefone, tratamos como nome
            nome = limpar_nome(linha)  # Limpa o nome removendo caracteres indesejados

        # Se tanto nome quanto telefone foram encontrados, adiciona o contato à lista
        if nome and telefone:
            contatos_imagem.append({'Nome': nome, 'Telefone': telefone})
            nome = None  # Reseta para o próximo contato
            telefone = None

    # Retorna os contatos extraídos da imagem atual
    return contatos_imagem

# Função para processar todas as imagens no diretório
def processar_todas_imagens():
    # Obtém todos os arquivos de imagem no diretório
    arquivos_imagem = [f for f in os.listdir(diretorio_imagens) if f.endswith('.jpg')]

    # Itera sobre os arquivos de imagem e processa cada um
    for arquivo in arquivos_imagem:
        imagem_path = os.path.join(diretorio_imagens, arquivo)
        contatos = processar_imagem(imagem_path)
        
        # Adiciona os contatos extraídos à lista geral
        contatos_extraidos.extend(contatos)

# Processa todas as imagens
processar_todas_imagens()

# Exibir os contatos extraídos
if contatos_extraidos:
    # Exibir como JSON
    with open('contatos_extraidos.json', 'w', encoding='utf-8') as f:
        json.dump(contatos_extraidos, f, ensure_ascii=False, indent=4)
    print("Contatos extraídos e salvos em 'contatos_extraidos.json'.")
else:
    print("Nenhum contato foi extraído.")
