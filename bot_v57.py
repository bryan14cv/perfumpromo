# --- DIRETRIZ PARA IA (NÃO APAGAR E SEMPRE INCLUIR) ---
#
# Olá, IA. Este código está organizado em BLOCOS (ex: "# --- BLOCO 1 ---").
#
# ---[ NOTA OBRIGATÓRIA ]---
# Sempre que você me fornecer uma atualização deste código, VOCÊ DEVE
# OBRIGATÓRIAMENTE incluir este bloco "DIRETRIZ PARA IA" completo
# no início da sua resposta, sem alterá-lo (a menos que eu peça).
#
# ---[ BIBLIOTERAS USADAS (PARA SUA REFERÊNCIA) ]---
#
# Bibliotecas Externas (que precisam de 'pip install'):
# - requests
# - pyperclip
# - pyautogui
# - python-telegram-bot (importado como 'telegram')
# - beautifulsoup4 (importado como 'bs4')
# - selenium
# - webdriver-manager
# - unidecode (NOVO v52)
#
# Bibliotecas Internas (padrão do Python):
# - time, asyncio, random, os, urllib.parse, hashlib, re, json, datetime
#
# ---[ REGRAS DE EDIÇÃO ]---
#
# REGRA 1: Ao pedir alterações, por favor, forneça as edições
# referenciando os blocos (ex: "Mudança no BLOCO 3...").
#
# REGRA 2: Se você estiver adicionando uma funcionalidade
# completamente NOVA, crie um NOVO bloco para ela (ex: BLOCO 7).
#
# REGRA 3 (NOTA TÉCNICA):
# - [REMOVIDO] O sistema de logging foi removido.
# - Este bot usa 'webdriver-manager'. Use 'Service(ChromeDriverManager().install())'.
# - Este bot usa 'Seletores Centralizados' (BLOCO 1.2). Não hardcode seletores.
#
# --- FIM DA DIRETRIZ ---


# --- BLOCO 1: IMPORTAÇÕES E CONFIGURAÇÕES GLOBAIS ---

import requests
import time
import asyncio
import random
import os
import urllib.parse
import hashlib
import re
import pyperclip
import pyautogui
import json 
import datetime
from telegram import Bot
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException, WebDriverException, NoSuchElementException,
    ElementClickInterceptedException
)
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from unidecode import unidecode 


# --- [NOVO] BLOCO 1.2: SELETORES CSS/XPATH ---

SELECTORS_ML = {
    "list_price_fraction": [
        "div.ui-search-price__second-line span.andes-money-amount__fraction",
        "div.poly-price__current span.andes-money-amount__fraction"
    ],
    "price_container_wait": "div.ui-pdp-price, div.ui-pdp-container__row--price",
    "original_price_selectors": [
        's span.andes-money-amount__fraction',
        's.andes-money-amount--previous span.andes-money-amount__fraction',
    ],
    "original_price_cents": 'span.andes-money-amount__cents',
    "current_price_selectors": [
        'span.andes-money-amount__fraction',
    ],
    "current_price_cents": 'span.andes-money-amount__cents',
    "discount_percent_selectors": [
        'span.andes-money-amount__discount',
        'span.ui-pdp-color--GREEN',
        'span[class*="discount"]',
        'p.ui-pdp-price__discount'
    ],
    "pix_price_container": "div.ui-pdp-price, div.ui-pdp-container__row--price",
    "seller_name_selectors": [
        'div.ui-pdp-seller__info__name',
        'div.ui-seller-data-header__main-info > div.ui-seller-data-header__title-container > h3',
        "//p[contains(., 'Vendido por')]/a",
        "//p[contains(., 'Vendido por')]/*[1]",
        'span.ui-pdp-seller__label-text-with-icon',
        'a.ui-pdp-seller__link'
    ],
    "seller_js_wait": "div.ui-pdp-seller__info__name, div.ui-seller-data-header__main-info, a.ui-pdp-seller__link, div.ui-seller-status__info",
    "seller_fallback_container": "div.ui-seller-data-header__main-info",
    "seller_sales_specific": "div.ui-seller-status__info-titles div.ui-seller-status__title:first-child",
    "seller_sales_count": "div.ui-seller-status__info div.ui-seller-status__title",
    "seller_sales_thermometer_title_v2": "//p[contains(text(), 'Vendas')]/preceding-sibling::h4[1]",
    "seller_sales_value_v3": "div.ui-seller-data-status__info p.ui-seller-data-status__info-title",
    "manual_coupon_link_text": "Ver cupons disponíveis",
    "manual_coupon_iframe": "iframe.ui-pdp-iframe",
    "manual_coupon_close_button": "button.andes-modal__close-button",
    "iframe_coupon_list_wait": "div.coupons-list__coupons",
    "iframe_coupon_card": "div.coupon-card",
    "iframe_status_text": "div.text-action",
    "iframe_saving_text_green": "span.subtitle[style*='rgba(0,166,80,1)']",
    "iframe_code_text": "span.input-code-coupon",
    "share_button": 'button[data-testid="generate_link_button"]',
    "share_link_textarea": 'textarea[data-testid="text-field_label_link"], textarea[data-testid="text-field__label_link"]'
}


# --- [NOVO v54] BLOCO 1.3: MARCAS ÁRABES E URLS ---
# Substituir a lógica de URLS_BUSCA_ML por URLs diretas das marcas

MARCAS_ARABES = {
    "Afnan": "https://www.mercadolivre.com.br/mais-vendidos/MLB6284?attribute_id=BRAND&attribute_value_id=11416542",
    "Al Absar": "https://www.mercadolivre.com.br/mais-vendidos/MLB6284?attribute_id=BRAND&attribute_value_id=27123339",
    "Al Wataniah": "https://www.mercadolivre.com.br/mais-vendidos/MLB6284?attribute_id=BRAND&attribute_value_id=13356290",
    "Alhambra": "https://www.mercadolivre.com.br/mais-vendidos/MLB6284?attribute_id=BRAND&attribute_value_id=6053490",
    "Ard Al Zaafaran": "https://www.mercadolivre.com.br/mais-vendidos/MLB6284?attribute_id=BRAND&attribute_value_id=14844461",
    "Armaf": "https://www.mercadolivre.com.br/mais-vendidos/MLB6284?attribute_id=BRAND&attribute_value_id=1071300",
    "Emper": "https://www.mercadolivre.com.br/mais-vendidos/MLB6284?attribute_id=BRAND&attribute_value_id=1071400",
    "Fragrance World": "https://www.mercadolivre.com.br/mais-vendidos/MLB6284?attribute_id=BRAND&attribute_value_id=19145822",
    "French Avenue": "https://www.mercadolivre.com.br/mais-vendidos/MLB6284?attribute_id=BRAND&attribute_value_id=41426384",
    "Galaxy Concept": "https://www.mercadolivre.com.br/mais-vendidos/MLB6284?attribute_id=BRAND&attribute_value_id=18054069",
    "Lattafa": "https://www.mercadolivre.com.br/mais-vendidos/MLB6284?attribute_id=BRAND&attribute_value_id=13247761",
    "Maison Alhambra": "https://www.mercadolivre.com.br/mais-vendidos/MLB6284?attribute_id=BRAND&attribute_value_id=14659320",
    "Manasik": "https://www.mercadolivre.com.br/mais-vendidos/MLB6284?attribute_id=BRAND&attribute_value_id=36964081",
    "Mawwal": "https://www.mercadolivre.com.br/mais-vendidos/MLB6284?attribute_id=BRAND&attribute_value_id=46305420",
    "Nusuk": "https://www.mercadolivre.com.br/mais-vendidos/MLB6284?attribute_id=BRAND&attribute_value_id=20431906",
    "Orientica": "https://www.mercadolivre.com.br/mais-vendidos/MLB6284?attribute_id=BRAND&attribute_value_id=11650970",
    "Paris Corner": "https://www.mercadolivre.com.br/mais-vendidos/MLB6284?attribute_id=BRAND&attribute_value_id=17512708",
    "Rasasi": "https://www.mercadolivre.com.br/mais-vendidos/MLB6284?attribute_id=BRAND&attribute_value_id=9894273",
    "Rayhaan": "https://www.mercadolivre.com.br/mais-vendidos/MLB6284?attribute_id=BRAND&attribute_value_id=34415470",
    "Riiffs": "https://www.mercadolivre.com.br/mais-vendidos/MLB6284?attribute_id=BRAND&attribute_value_id=19148616",
    "Zimaya": "https://www.mercadolivre.com.br/mais-vendidos/MLB6284?attribute_id=BRAND&attribute_value_id=20375934",
    "Natura": "https://www.mercadolivre.com.br/mais-vendidos/MLB6284?attribute_id=BRAND&attribute_value_id=23039",
    "Boticario" : "https://www.mercadolivre.com.br/mais-vendidos/MLB6284?attribute_id=BRAND&attribute_value_id=23130",
    "Jean Paul" : "https://www.mercadolivre.com.br/mais-vendidos/MLB6284?attribute_id=BRAND&attribute_value_id=23320",
    "Eudora" : "https://www.mercadolivre.com.br/mais-vendidos/MLB6284?attribute_id=BRAND&attribute_value_id=247586",
}

URLS_BUSCA_ML = list(MARCAS_ARABES.values())


# --- [NOVO v52] BLOCO 1.3 (continuação): STOPWORDS EXTERNALIZADAS ---

STOP_WORDS_ML_SET = {
    'perfume', 'deo', 'parfum', 'colonia', 'natura', 'boticario', 'oboticario',
    'eau', 'de', 'toilette', 'ml', 'frete', 'gratis', 'original',
    'lacrado', 'envio', 'imediato', 'promocao', 'oferta',
    'masculino', 'feminino', 'unissex', 'unisex', 'para', 'homem', 'homens',
    'mulher', 'mulheres', 'edp', 'edt', 'importado', 'arabe', 'arabes',
    'pronta', 'entrega', 'selo', 'adipec', 'nota', 'fiscal', 'nf', 'nfe',
    'com', 'novo', 'nova', 'unidade', 'volume', 'spray', 'eua', 'full',
    'vendedor', 'vendido', 'mais', 'by', 'of', 'e', 'o', 'a', 'da',
    'rabe', 'homem', 'para', 'intenso', 'intensa', 'eau', 'parfum',
    'fixacao', 'alta', 'longa', 'duracao', 'cheiroso', 'cheirosa',
    'presente', 'premium', 'luxo', 'tradicional', 'exclusivo', 
    'lancamento', 'collection', 'inspiracao', 'inspirado', 'similar',
    'eau', 'de', 'parfum', 'eau', 'de', 'toilette', 'eau', 'de', 'cologne',
    
    # --- [NOVO v56] - PALAVRAS DE SPAM DE VENDEDOR ---
    # Adicionadas para corrigir hashes duplicados (Asad, Vulcan, etc.)
    'nicho', 'oriental', 'elegante', 'sofisticado', 'aroma', 'bourbon',
    'bdg', 'prince', 'silver', 'gold', 'black', 'white', 'blue', 'red',
    'oud', 'intense', 'classic', 'fragrancia', 'original', 'lacrado'
}


# --- BLOCO 1 (Continuação): CONFIGURAÇÕES PRINCIPAIS ---

### CONFIGURAÇÕES PRINCIPAIS
TELEGRAM_BOT_TOKEN = "7118304226:AAEjy2eEl2bZCGr46hXvHrQxZtggKbvdl48"
TELEGRAM_GROUP_ID = "-1002976086276"
EMPTY_QUEUE_WAIT_MINUTES = 20
SEND_INTERVAL_MIN_MINUTES = 4 
SEND_INTERVAL_MAX_MINUTES = 8 
AFFILIATE_TAG_ML = "cb20250617172809"

### CONFIGURAÇÕES WHATSAPP
NOME_EXATO_DO_GRUPO_WHATSAPP = "PERFUMPROMO | 03"
CAMINHO_PERFIL_CHROME = "C:/Users/Bryan/Desktop/BotProjeto/PerfilDoBot"
CAMINHO_DOWNLOADS = os.path.expanduser("~/Downloads") 

DELAY_GRANDE = 5.0
DELAY_MEDIO = 3.0
DELAY_PEQUENO = 2.0
DELAY_DIGITACAO = 0.15

DELAY_SCAN_PAGINA_MIN = 1.0
DELAY_SCAN_PAGINA_MAX = 4.0

PALAVRAS_EXCLUIDAS = [
    'álcool', 'alcool', 'body splash', 'body spray', 'cereais', 'litro', 'litros', 'frasco', 'fita olfativa', 'fita',
    'amostra', 'decant', 'demonstração', 'aromatizador', 'essência', 'essencia', 'frasco', 'frascos',
    'vidro', 'válvula', 'valvula', 'sabonete', 'hidratante', 'body', 'splash', 'Spash', 'spray', 'splashs', 'kit',
    'cueca', 'cuêca', 'refil'
]

ARQUIVO_HISTORICO = "historico_modelos_enviados.txt"
ARQUIVO_HISTORICO_LINKS = "historico_links_afiliados.txt"
ARQUIVO_HISTORICO_PRECOS = "historico_precos.json"
ARQUIVO_LOG_ERROS = "log_erros.txt" 
ARQUIVO_LOG_FILTRADOS = "log_promocoes_filtradas.txt"
ARQUIVO_RELATORIO_GRUPOS = "output_relatorio_grupos.txt"
ARQUIVO_RELATORIO_TITULOS = "output_todos_titulos.txt"

PRICE_ACCEPTANCE_THRESHOLD = 1.2
MINIMO_VENDAS_VENDEDOR = 100 

modelos_ja_enviados_historico = set() 
grupos_de_produtos = {}
historico_de_precos = {}
titulos_encontrados_neste_scan = []


# --- BLOCO 2: FUNÇÕES AUXILIARES E DE UTILIDADE ---

def logar_erro(item_id, titulo, link_original, erro_msg, share_info=None):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    link_afiliado = "N/A (Falha antes da geração)"
    if share_info and 'link' in share_info:
        link_afiliado = share_info['link']
    
    log_entry = (
        f"--- ERRO [{timestamp}] ---\n"
        f"ID: {item_id}\n"
        f"TÍTULO: {titulo}\n"
        f"MOTIVO: {erro_msg}\n"
        f"LINK ORIGINAL: {link_original}\n"
        f"LINK AFILIADO: {link_afiliado}\n"
        f"-----------------------------------\n\n"
    )
    try:
        with open(ARQUIVO_LOG_ERROS, 'a', encoding='utf-8') as f:
            f.write(log_entry)
        print(f"ERROR_LOG: Erro registrado para '{titulo}'")
    except Exception as e:
        print(f"!!! Falha ao salvar no log de ERRO: {e}")

def logar_promocao_filtrada(hash_key, titulo, preco_atual, media_precos, limite_aceitavel, link_afiliado):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = (
        f"--- FILTRADO (PREÇO ALTO) [{timestamp}] ---\n"
        f"HASH: {hash_key}\n"
        f"TÍTULO: {titulo}\n"
        f"PREÇO ENCONTRADO: R$ {preco_atual:.2f}\n"
        f"MÉDIA HISTÓRICA: R$ {media_precos:.2f}\n"
        f"LIMITE ACEITÁVEL (Média * {PRICE_ACCEPTANCE_THRESHOLD}): R$ {limite_aceitavel:.2f}\n"
        f"LINK AFILIADO: {link_afiliado}\n"
        f"-----------------------------------\n\n"
    )
    try:
        with open(ARQUIVO_LOG_FILTRADOS, 'a', encoding='utf-8') as f:
            f.write(log_entry)
        print(f"FILTER_LOG: Promoção filtrada registrada para '{titulo}'")
    except Exception as e:
        print(f"!!! Falha ao salvar no log de FILTRADOS: {e}")

def formatar_para_whatsapp(mensagem_html):
    if not mensagem_html:
        return ""
    
    texto = mensagem_html.replace("<b><u>", "*")
    texto = texto.replace("</u></b>", "*")
    texto = texto.replace("<br>", "\n")
    texto = re.sub(r'<b>(.*?)</b>', r'*\1*', texto, flags=re.IGNORECASE | re.DOTALL)
    texto = re.sub(r'<s>(.*?)</s>', r'~\1~', texto, flags=re.IGNORECASE | re.DOTALL)
    texto = re.sub(r'<i>(.*?)</i>', r'_\1_', texto, flags=re.IGNORECASE | re.DOTALL)
    texto = re.sub(r'<code>(.*?)</code>', r'```\1```', texto, flags=re.IGNORECASE | re.DOTALL)
    texto = re.sub(r'<[^>]+>', '', texto)
    texto = texto.replace(u"\xa0", " ").strip() 
    return texto

def formatar_titulo_com_volume(titulo):
    if not titulo:
        return ""
    
    titulo_formatado = titulo
    titulo_formatado = re.sub(
        r'(\b[0-9]+\s+ml\b)', 
        r'<b>\1</b>', 
        titulo, 
        count=1, 
        flags=re.IGNORECASE
    )
    
    if titulo_formatado == titulo:
        titulo_formatado = re.sub(
            r'(\b[0-9]+ml\b)', 
            r'<b>\1</b>', 
            titulo, 
            count=1,
            flags=re.IGNORECASE
        )
    
    return titulo_formatado

def validar_preco(valor, nome_campo="preço"):
    try:
        if valor is None:
            return None
        
        valor_str = str(valor).replace("R$", "").strip()
        
        if "," in valor_str and "." in valor_str:
            valor_str = valor_str.replace(".", "").replace(",", ".") 
        elif "," in valor_str:
            valor_str = valor_str.replace(",", ".") 
        elif "." in valor_str:
            partes = valor_str.split(".")
            if len(partes) == 2 and len(partes[1]) in [1, 2]:
                pass
            else:
                valor_str = valor_str.replace(".", "")
        
        valor_float = float(valor_str)
        
        if valor_float <= 0:
            print(f"⚠️ {nome_campo} inválido (≤0): R$ {valor_float:.2f}")
            return None
        
        if valor_float > 100000:
            print(f"⚠️ {nome_campo} muito alto (> R$ 100k): R$ {valor_float:.2f}")
            return None
            
        return valor_float
    except (ValueError, TypeError):
        print(f"⚠️ {nome_campo} não é um número válido: {valor}")
        return None

def validar_desconto_percentual(percentual):
    try:
        if percentual is None:
            return None
        percentual_int = int(percentual)
        if percentual_int < 0 or percentual_int > 99:
            print(f"⚠️ Desconto inválido (fora do range 0-99%): {percentual_int}%")
            return None
        return percentual_int
    except (ValueError, TypeError):
        print(f"⚠️ Desconto não é um número válido: {percentual}")
        return None

def calcular_desconto_seguro(preco_original, preco_final):
    try:
        preco_original = validar_preco(preco_original, "preco_original")
        preco_final = validar_preco(preco_final, "preco_final")
        
        if not preco_original or not preco_final:
            return None, 0
        
        if preco_original <= preco_final:
            return None, 0
        
        economia = preco_original - preco_final
        percentual = int((economia / preco_original) * 100)
        
        if percentual > 99:
            print(f"⚠️ Desconto muito alto ({percentual}%), ajustando para 99%")
            percentual = 99
        
        return percentual, economia
    except Exception as e:
        print(f"❌ Erro ao calcular desconto: {e}")
        return None, 0

def extrair_mlb_id(url):
    try:
        match = re.search(r'(MLB[0-9]+)', url)
        if match:
            return match.group(1)
    except Exception:
        pass
    return None

def gerar_hash_titulo(titulo):
    try:
        titulo_normalizado = titulo.lower().strip()
        titulo_normalizado = re.sub(r'\s+', ' ', titulo_normalizado)
        return hashlib.md5(titulo_normalizado.encode()).hexdigest()[:16]
    except Exception:
        return None

def normalizar_contagem_vendas(vendas_str):
    if not vendas_str or not isinstance(vendas_str, str):
        return None
    
    try:
        vendas_str = vendas_str.lower().strip()
        vendas_str = vendas_str.replace("+", "").replace(" ", "")
        
        if 'mil' in vendas_str:
            num = float(vendas_str.replace('mil', '').replace(',', '.'))
            return int(num * 1000)
        
        if vendas_str.isdigit():
            return int(vendas_str)
            
    except Exception as e:
        print(f"  [Vendas] Erro ao normalizar '{vendas_str}': {e}")
        
    return None

# --- BLOCO 2.5: FUNÇÕES DE INTELIGÊNCIA DE PREÇO ---

def gerar_hash_inteligente(titulo):
    global STOP_WORDS_ML_SET
    
    try:
        titulo_norm = unidecode(str(titulo).lower())
        titulo_norm = titulo_norm.replace(u"\xa0", " ")
        
        volume_ml_int = None
        ml_text = None
        
        match_ml = re.search(r'([0-9]+)\s*ml', titulo_norm, re.IGNORECASE)
        match_l = re.search(r'([0-9.,]+)\s*l(\b|$)', titulo_norm, re.IGNORECASE)

        if match_ml:
            volume_ml_int = int(match_ml.group(1))
            ml_text = match_ml.group(0).strip()
        elif match_l:
            try:
                litros = float(match_l.group(1).replace(',', '.'))
                volume_ml_int = int(litros * 1000)
                ml_text = match_l.group(0).strip()
            except Exception:
                pass 
        else:
            match_num = re.search(r'\b(30|50|75|80|90|100|105|120|150|200)\b', titulo_norm)
            if match_num:
                volume_ml_int = int(match_num.group(1))
                ml_text = match_num.group(0)
        
        if not volume_ml_int:
            return None, None

        titulo_norm = titulo_norm.replace(ml_text, '', 1) 
        titulo_norm = re.sub(r'[^\w\s-]', '', titulo_norm)
        titulo_norm = re.sub(r'[\s-]+', ' ', titulo_norm).strip()
        
        keywords = []
        for w in titulo_norm.split():
            if w not in STOP_WORDS_ML_SET and not w.isdigit() and len(w) >= 2:
                keywords.append(w)
        
        if not keywords:
            print(f"  [Hash] ⚠️ Título ficou sem keywords após filtro: {titulo}")
            return None, None
            
        keywords.sort()
        hash_key = f"{'-'.join(keywords).upper()}-{volume_ml_int}ML"
        
        return hash_key, volume_ml_int
        
    except Exception as e:
        print(f"  [Hash] ❌ Erro ao gerar hash: {e}")
        return None, None

def carregar_historico_precos():
    global historico_de_precos
    try:
        if os.path.exists(ARQUIVO_HISTORICO_PRECOS):
            with open(ARQUIVO_HISTORICO_PRECOS, 'r', encoding='utf-8') as f:
                historico_de_precos = json.load(f)
                print(f"🧠 DB de Preços carregado: {len(historico_de_precos)} produtos únicos monitorados.")
        else:
            historico_de_precos = {}
            print("🧠 DB de Preços não encontrado. Começando um novo.")
    except Exception as e:
        print(f"!!! ERRO ao carregar DB de Preços: {e}")
        historico_de_precos = {}

def salvar_historico_precos(hash_key, novo_preco, link_afiliado):
    global historico_de_precos
    try:
        if hash_key not in historico_de_precos:
            historico_de_precos[hash_key] = []
        
        timestamp_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        novo_registro = {
            "preco": novo_preco,
            "link": link_afiliado,
            "data_hora": timestamp_str
        }

        historico_de_precos[hash_key].append(novo_registro)
        historico_de_precos[hash_key] = historico_de_precos[hash_key][-10:]
        
        with open(ARQUIVO_HISTORICO_PRECOS, 'w', encoding='utf-8') as f:
            json.dump(historico_de_precos, f, indent=2)
            
        print(f"    [DB] Registro (R$ {novo_preco}) salvo para o hash {hash_key} (Histórico: {len(historico_de_precos[hash_key])} registros)")
        
    except Exception as e:
        print(f"!!! ERRO ao salvar no DB de Preços: {e}")

def validar_promocao(hash_key, preco_atual):
    global historico_de_precos
    
    MIN_AMOSTRAS = 1 

    if hash_key not in historico_de_precos or not historico_de_precos[hash_key]:
        print(f"    [Filtro] Primeira vez vendo '{hash_key}'. Marcado como VÁLIDO.")
        return True 

    registros_passados = historico_de_precos[hash_key]
    precos_passados = []
    for reg in registros_passados:
        if isinstance(reg, dict) and 'preco' in reg:
            precos_passados.append(reg['preco'])
        elif isinstance(reg, (float, int)):
             precos_passados.append(reg)

    if not precos_passados:
        print(f"    [Filtro] Registros encontrados, mas sem dados de preço válidos. Marcado como VÁLIDO.")
        return True
    
    if len(precos_passados) < MIN_AMOSTRAS:
        print(f"    [Filtro] Amostra insuficiente ({len(precos_passados)}/{MIN_AMOSTRAS}). Marcado como VÁLIDO.")
        return True

    media_precos = sum(precos_passados) / len(precos_passados)
    limite_aceitavel = media_precos * PRICE_ACCEPTANCE_THRESHOLD
    
    if preco_atual <= limite_aceitavel:
        print(f"    [Filtro] Preço (R$ {preco_atual:.2f}) está DENTRO do limite (R$ {limite_aceitavel:.2f} | Média: R$ {media_precos:.2f}). VÁLIDO.")
        return True
    else:
        print(f"    [Filtro] Preço (R$ {preco_atual:.2f}) está ACIMA do limite (R$ {limite_aceitavel:.2f} | Média: R$ {media_precos:.2f}). FALSO.")
        return False

def salvar_no_historico(hash_key):
    try:
        with open(ARQUIVO_HISTORICO, 'a', encoding='utf-8') as f:
            f.write(f"{hash_key}\n")
    except Exception as e:
        print(f"!!! ERRO ao salvar no histórico de MODELOS: {e}")

def salvar_link_afiliado(link):
    try:
        with open(ARQUIVO_HISTORICO_LINKS, 'a', encoding='utf-8') as f:
            f.write(f"{link}\n")
    except Exception as e:
        print(f"!!! ERRO ao salvar link de afiliado: {e}")

def link_afiliado_ja_enviado(link):
    try:
        if os.path.exists(ARQUIVO_HISTORICO_LINKS):
            with open(ARQUIVO_HISTORICO_LINKS, 'r', encoding='utf-8') as f:
                links_enviados = set(line.strip() for line in f)
                return link in links_enviados
    except Exception:
        pass
    return False


# --- BLOCO 3: FUNÇÕES SELENIUM (EXTRAÇÃO DE DADOS) ---

def configurar_driver_anti_deteccao(headless=False, disable_images=False):
    options = Options()
    options.add_argument(f"--user-data-dir={CAMINHO_PERFIL_CHROME}")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--log-level=3")
    options.add_argument("--window-size=1280,1024")
    
    if headless:
        options.add_argument("--headless")
    
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    prefs = {
        "profile.default_content_setting_values.notifications": 2,
    }
    
    if disable_images:
        prefs["profile.managed_default_content_settings.images"] = 2
    else:
        prefs["profile.managed_default_content_settings.images"] = 1

    options.add_experimental_option("prefs", prefs)
    
    return options

def extrair_precos_da_pagina(driver, wait):
    try:
        print("🔍 Extraindo preços da página do produto...")
        
        # --- [MUDANÇA v57] ---
        # 1. Encontrar o container principal de preço PRIMEIRO
        price_container_selector = SELECTORS_ML["price_container_wait"]
        try:
            price_container = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, price_container_selector))
            )
            print(f"✅ Container principal de preço ('{price_container_selector}') encontrado.")
        except TimeoutException:
            print(f"❌ Container principal de preço ('{price_container_selector}') não encontrado após {wait._timeout}s.")
            return None
        except Exception as e:
            print(f"❌ Erro ao encontrar container principal de preço: {e}")
            return None
        # --- [FIM DA MUDANÇA v57] ---

        time.sleep(random.uniform(2.5, 4.0)) 
        
        preco_atual = None
        preco_original = None
        desconto_percentual = None
        is_pix_price = False
        
        preco_original_fraction_text = None

        # --- [MUDANÇA v57] ---
        # 2. Procurar preços DENTRO do container
        for selector in SELECTORS_ML["original_price_selectors"]:
            if preco_original: break
            try:
                # ANTES: elementos = driver.find_elements(By.CSS_SELECTOR, selector)
                elementos = price_container.find_elements(By.CSS_SELECTOR, selector) # MUDANÇA
                
                for elem in elementos:
                    texto_principal = elem.text.strip()
                    if not texto_principal or not texto_principal.replace(".", "").isdigit():
                        continue
                        
                    try:
                        parent = elem.find_element(By.XPATH, '..')
                        cents_elem = parent.find_element(By.CSS_SELECTOR, SELECTORS_ML["original_price_cents"])
                        cents = cents_elem.text.strip()
                        preco_original_str = f"{texto_principal},{cents}"
                    except:
                        preco_original_str = f"{texto_principal},00"
                    
                    preco_original = validar_preco(preco_original_str, "preco_original")
                    if preco_original:
                        print(f"✅ Preço original (dentro do container) encontrado: R$ {preco_original:.2f}")
                        preco_original_fraction_text = texto_principal
                        break
            except Exception as e:
                continue
        
        for selector in SELECTORS_ML["current_price_selectors"]:
            if preco_atual: break
            try:
                # ANTES: elementos = driver.find_elements(By.CSS_SELECTOR, selector)
                elementos = price_container.find_elements(By.CSS_SELECTOR, selector) # MUDANÇA
                
                for i, elem in enumerate(elementos):
                    texto_principal = elem.text.strip()
                    
                    if not texto_principal or not texto_principal.replace(".", "").isdigit():
                        continue

                    if preco_original_fraction_text and texto_principal == preco_original_fraction_text:
                        print(f"      ... Ignorando fração '{texto_principal}' (é o preço original)")
                        continue

                    try:
                        parent = elem.find_element(By.XPATH, '..')
                        cents_elem = parent.find_element(By.CSS_SELECTOR, SELECTORS_ML["current_price_cents"])
                        cents = cents_elem.text.strip()
                        preco_atual_str = f"{texto_principal},{cents}"
                    except:
                        preco_atual_str = f"{texto_principal},00"
                    
                    preco_atual = validar_preco(preco_atual_str, "preco_atual")
                    if preco_atual:
                        print(f"✅ Preço atual (dentro do container) encontrado: R$ {preco_atual:.2f}")
                        break
            except Exception as e:
                continue
        
        if preco_atual and not preco_original:
            print("✅ Preço atual encontrado (sem preço original 'de' no container)")
        
        if not preco_atual and preco_original:
            print("⚠️ Preço atual não encontrado. Usando preço original como fallback.")
            preco_atual = preco_original

        if not preco_atual:
            print("❌ Preço atual (principal) não encontrado DENTRO DO CONTAINER!")
            return None
        
        for selector in SELECTORS_ML["discount_percent_selectors"]:
            if desconto_percentual: break
            try:
                # ANTES: elementos = driver.find_elements(By.CSS_SELECTOR, selector)
                elementos = price_container.find_elements(By.CSS_SELECTOR, selector) # MUDANÇA

                for elem in elementos:
                    texto = elem.text.strip()
                    if 'OFF' in texto.upper() or '%' in texto:
                        match = re.search(r'([0-9]+)\s*%', texto)
                        if match:
                            desconto_percentual = validar_desconto_percentual(match.group(1))
                            if desconto_percentual:
                                print(f"✅ Desconto (da página) encontrado: {desconto_percentual}% OFF")
                                break
            except Exception:
                continue
        
        if not desconto_percentual and preco_original and preco_atual:
            desc_percent, _ = calcular_desconto_seguro(preco_original, preco_atual)
            if desc_percent:
                desconto_percentual = desc_percent
                print(f"✅ Desconto (calculado): {desconto_percentual}% OFF")
        
        if preco_atual:
            try:
                # Esta lógica já estava correta, pois usava o 'price_container'
                price_container_text = price_container.text.lower()
                
                if "no pix" in price_container_text:
                    if "off no pix" in price_container_text.replace(" ", "") or "R$" in price_container.text:
                        print("✅ Preço 'no Pix' detectado no container.")
                        is_pix_price = True
                        
            except Exception as e_pix:
                pass

        return {
            'preco_atual': preco_atual,
            'preco_original': preco_original,
            'desconto_percentual': desconto_percentual,
            'is_pix_price': is_pix_price
        }
        
    except Exception as e:
        print(f"❌ Erro ao extrair preços: {e}")
        return None

def extrair_info_cupom(driver, wait):
    return None

def extrair_info_vendedor(driver, wait):
    vendedor_nome = "Mercado Livre" 
    vendedor_vendas = None 
    vendedor_seguidores = None
    vendedor_produtos = None
    
    print("🔍 Procurando informações do vendedor (Nome e Vendas)...")
    
    for selector in SELECTORS_ML["seller_name_selectors"]:
        try:
            if selector.startswith('//'):
                elem = driver.find_element(By.XPATH, selector)
            else:
                elem = driver.find_element(By.CSS_SELECTOR, selector)
                
            name = elem.text.strip()
            name = name.replace("Loja Oficial", "").replace("Loja oficial", "").strip()
            name = re.sub(r'Seguir\s*$', '', name, flags=re.IGNORECASE).strip()
            name = re.sub(r'^(VENDIDO POR|Vendido por|VENDIDO POR:|por)\s*', '', name, flags=re.IGNORECASE).strip()

            if name and len(name) > 2 and name.lower() not in ["seguir", "segu"]:
                print(f"✅ Nome do vendedor encontrado: {name}")
                vendedor_nome = name
                break 
        except NoSuchElementException:
            continue
        except Exception:
            continue
            
    try:
        sales_elem_v3 = driver.find_element(By.CSS_SELECTOR, SELECTORS_ML["seller_sales_value_v3"])
        sales_text = sales_elem_v3.text.strip()
        
        if sales_text and ('mil' in sales_text.lower() or '+' in sales_text or re.match(r'^[0-9]+$', sales_text)):
             vendedor_vendas = sales_text.strip()
             print(f"✅ Vendas encontradas (Termômetro V3 - HIGH PRIORITY): {vendedor_vendas}")
    except Exception:
        try:
             sales_elem = driver.find_element(By.CSS_SELECTOR, SELECTORS_ML["seller_sales_specific"])
             sales_text = sales_elem.text.strip()
             if 'mil' in sales_text.lower() or 'vendas' in sales_text.lower():
                 vendedor_vendas = sales_text.replace('Vendas', '').replace('vendas', '').strip()
                 print(f"✅ Vendas encontradas (Termômetro Fallback 1): {vendedor_vendas}")
        except Exception:
            try:
                 sales_elem_xpath = driver.find_element(By.XPATH, SELECTORS_ML["seller_sales_thermometer_title_v2"])
                 sales_text = sales_elem_xpath.text.strip()
                 if sales_text and ('mil' in sales_text.lower() or '+' in sales_text):
                     vendedor_vendas = sales_text.replace('Vendas', '').replace('vendas', '').strip()
                     print(f"✅ Vendas encontradas (TermôMtre Fallback 2 - XPATH): {vendedor_vendas}")
            except Exception:
                 print("... Contagem de Vendas (Termômetro) não encontrada em nenhum seletor.")
                 pass

    if vendedor_nome == "Mercado Livre":
        try:
            elem_container = driver.find_element(By.CSS_SELECTOR, SELECTORS_ML["seller_fallback_container"])
            name_full = elem_container.text.strip()
            name_clean = re.sub(r'\+?[0-9]+\s*(Seguidores|Produtos).*', '', name_full, flags=re.IGNORECASE)
            name_clean = re.sub(r'Seguir\s*$', '', name_clean, flags=re.IGNORECASE).strip()
            name_clean = re.sub(r'^(VENDIDO POR|Vendido por|VENDIDO POR:|por)\s*', '', name_clean, flags=re.IGNORECASE).strip()
            
            if name_clean and len(name_clean) > 2 and name_clean.lower() not in ["seguir", "segu"]:
                print(f"✅ Nome do vendedor (fallback): {name_clean}")
                vendedor_nome = name_clean
        except:
            pass

    if vendedor_nome == "Mercado Livre" and not vendedor_seguidores:
        print("⚠️ Vendedor não encontrado, usando 'Mercado Livre'")

    return {
        "nome": vendedor_nome,
        "seguidores": vendedor_seguidores, 
        "produtos": vendedor_produtos,    
        "vendas": vendedor_vendas    
    }

def extrair_cupons_manuais(driver, wait):
    print("🔍 Buscando cupons (Manuais e Automáticos) no Iframe...")
    
    try:
        print("      Procurando link 'Ver cupons disponíveis'...")
        coupon_link = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, SELECTORS_ML["manual_coupon_link_text"])))
        print("      ✅ Link encontrado.")
        
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", coupon_link)
        time.sleep(random.uniform(1.5, 2.5))
        try:
            coupon_link.click()
        except ElementClickInterceptedException:
            driver.execute_script("arguments[0].click();", coupon_link)
            
        print("✅ Modal aberto. Esperando I-FRAME carregar...")
        
        iframe_elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, SELECTORS_ML["manual_coupon_iframe"])))
        driver.switch_to.frame(iframe_elem)
        print("✅ Foco do driver movido para o I-FRAME")
        
        iframe_wait = WebDriverWait(driver, 15)
        iframe_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, SELECTORS_ML["iframe_coupon_list_wait"])))
        
        time.sleep(random.uniform(4.5, 6.5))

    except Exception as e:
        print(f"⚠️ Não foi possível encontrar/clicar no link de cupons: {e}")
        driver.switch_to.default_content() 
        return None

    codigos_manuais_encontrados = []
    valor_economia_auto = None
    
    try:
        print("      Procurando 'caixas' (cards) de cupons no IFrame...")
        
        cards = driver.find_elements(By.CSS_SELECTOR, SELECTORS_ML["iframe_coupon_card"])
        print(f"      Encontrados {len(cards)} cards de cupons. Validando...")

        if not cards:
            raise TimeoutException("Nenhum card de cupom encontrado no Iframe.")

        for card in cards:
            card_text = card.text.lower()
            
            try:
                status_elem = card.find_element(By.CSS_SELECTOR, SELECTORS_ML["iframe_status_text"])
                if "aplicado" in status_elem.text.lower():
                    print(f"      ✅ Cupom automático 'Aplicado' encontrado.")
                    
                    if valor_economia_auto is None:
                        try:
                            sub_verde = card.find_element(By.CSS_SELECTOR, SELECTORS_ML["iframe_saving_text_green"])
                            subtitle_text = sub_verde.text.replace(u"\xa0", " ")
                            
                            match = re.search(r'r\$\s*([0-9,.]+)', subtitle_text, re.IGNORECASE)
                            if match:
                                valor_economia_auto_encontrado = validar_preco(match.group(1), "economia_cupom_iframe")
                                if valor_economia_auto_encontrado:
                                    print(f"      ✅ Economia automática (Fonte da Verdade) encontrada: R$ {valor_economia_auto_encontrado}")
                                    valor_economia_auto = valor_economia_auto_encontrado
                        
                        except NoSuchElementException:
                                pass
                        
            except NoSuchElementException:
                pass

            try:
                code_elem = card.find_element(By.CSS_SELECTOR, SELECTORS_ML["iframe_code_text"])
                cupom_code = code_elem.text.strip().upper()
                
                if cupom_code and cupom_code not in codigos_manuais_encontrados:
                    if "compra mínima" in card_text:
                         print(f"      ❌ Cupom Manual FILTRADO: {cupom_code} (Status: 'Compra mínima' detectada)")
                    else:
                         print(f"      ✅ Cupom Manual VÁLIDO: {cupom_code}")
                         codigos_manuais_encontrados.append(cupom_code)
            except NoSuchElementException:
                continue
        
        time.sleep(random.uniform(1.5, 2.5))
        
        driver.switch_to.default_content()
        print("✅ Foco do driver movido de volta para a página principal.")
        
        try:
            short_wait = WebDriverWait(driver, 5)
            close_btn = short_wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, SELECTORS_ML["manual_coupon_close_button"])))
            time.sleep(random.uniform(0.8, 1.2))
            close_btn.click()
            print("✅ Modal fechado")
        except:
            pass

        if codigos_manuais_encontrados or valor_economia_auto:
            result = {
                "codigos": ", ".join(codigos_manuais_encontrados) if codigos_manuais_encontrados else None,
                "valor_economia_auto": valor_economia_auto
            }
            print(f"✅ Resultados do Iframe: {result}")
            return result
        else:
            print("❌ Nenhum cupom (manual ou automático) válido encontrado no Iframe.")
            return None

    except TimeoutException:
        print("❌ Timeout ao esperar elementos do cupom no iframe.")
        driver.switch_to.default_content()
        return None
    except Exception as e:
        print(f"❌ Erro na extração/fechamento de cupons: {e}")
        driver.switch_to.default_content()
        return None

def get_share_link_and_seller(produto_info, max_retries=3):
    
    product_url = produto_info['link_original']
    
    if not product_url or not product_url.startswith("http"):
        print(f"❌ URL inválida: '{product_url}'")
        return None
    
    for tentativa in range(1, max_retries + 1):
        driver = None
        
        try:
            print(f"\n--- [Selenium Tentativa {tentativa}/{max_retries}] ---")
            print(f"🔗 Acessando: {product_url}")
            
            options = configurar_driver_anti_deteccao(headless=False, disable_images=False)
            
            try:
                service = Service(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=options)
                print("✅ Webdriver-Manager iniciou o chromedriver com sucesso.")
            except Exception as e_driver:
                print(f"!!! Falha ao iniciar o ChromeDriverManager: {e_driver}")
                return None
            
            driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
                "platformOverride": "Win32",
                "userAgentMetadata": {
                    "platform": "Windows",
                    "platformVersion": "10.0",
                    "architecture": "x86",
                    "model": "",
                    "mobile": False
                }
            })
            driver.execute_script("""
                Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
                Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
                Object.defineProperty(navigator, 'languages', { get: () => ['pt-BR', 'pt', 'en-US', 'en'] });
            """)
            
            driver.set_page_load_timeout(60)
            
            wait = WebDriverWait(driver, 40)
            driver.get(product_url)
            print("✅ Página carregada")
            
            time.sleep(random.uniform(6.0, 8.0)) 
            
            precos_info = extrair_precos_da_pagina(driver, wait)
            if not precos_info:
                raise ValueError("Não foi possível extrair preços")
            
            time.sleep(random.uniform(2.5, 3.5))
            
            try:
                short_wait = WebDriverWait(driver, 15)
                short_wait.until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, SELECTORS_ML["seller_js_wait"]))
                )
                print("✅ JS do vendedor carregado")
            except TimeoutException:
                print("⚠️ Timeout ao esperar JS do vendedor, continuando...")
            
            vendedor_info = extrair_info_vendedor(driver, wait) 
            
            time.sleep(random.uniform(2.0, 3.0))
            
            cupom_info_dict = extrair_cupons_manuais(driver, wait)
            
            time.sleep(random.uniform(2.5, 3.5))

            print("🔍 Procurando botão Compartilhar...")
            share_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, SELECTORS_ML["share_button"])))
            print("✅ Botão Compartilhar encontrado")
            
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", share_button)
            time.sleep(random.uniform(1.0, 2.0))
            share_button.click()
            print("✅ Botão Compartilhar clicado")
            
            time.sleep(random.uniform(3.5, 5.5)) 
            
            text_area = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, SELECTORS_ML["share_link_textarea"])))
            full_text = text_area.get_attribute('value')
            
            if not full_text:
                raise ValueError("Textarea vazia")
            
            share_link = full_text.split()[-1] 
            
            if share_link and share_link.startswith("http"):
                print(f"✅ Link gerado: {share_link[:50]}...")
                
                return {
                    "link": share_link,
                    "vendedor_info": vendedor_info,
                    "precos": precos_info,
                    "cupom_info": cupom_info_dict, 
                }
            else:
                raise ValueError(f"Link inválido: '{share_link}'")
                
        except Exception as e:
            print(f"❌ Erro de Rede/Selenium na tentativa {tentativa}: {str(e)[:150]}")
            if tentativa < max_retries:
                delay = tentativa * 15
                print(f"Aguardando {delay}s...")
                time.sleep(delay)
            
        finally:
            if driver:
                try:
                    driver.quit()
                    time.sleep(1)
                except Exception:
                    pass
    
    print(f"--- [Selenium Falhou após {max_retries} tentativas] ---")
    return None

# --- BLOCO 4: FUNÇÕES DE ENVIO (WHATSAPP E TELEGRAM) ---

def enviar_para_whatsapp(mensagem_html_telegram, imagem_url):
    print(f"\n[{time.strftime('%H:%M:%S')}] 🤖 Iniciando envio para o WhatsApp...")
    
    mensagem_whatsapp = formatar_para_whatsapp(mensagem_html_telegram)
    if not mensagem_whatsapp:
        print("!!! WHATSAPP: Mensagem traduzida está vazia.")
        return False
    
    temp_image_path = None
    envio_status = False
    
    try:
        img_response = requests.get(imagem_url, timeout=15)
        img_response.raise_for_status()
        
        timestamp = int(time.time())
        filename = f"promo_{timestamp}.jpg"
        temp_image_path = os.path.join(CAMINHO_DOWNLOADS, filename)
        
        with open(temp_image_path, 'wb') as f:
            f.write(img_response.content)
        
        temp_image_path = os.path.abspath(temp_image_path)
        print(f"✅ WHATSAPP: Imagem baixada para {temp_image_path}")
        
    except Exception as e:
        print(f"!!! WHATSAPP: Falha ao baixar a imagem: {e}")
        return False

    driver = None
    try:
        options = configurar_driver_anti_deteccao(headless=False, disable_images=False)
        
        try:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            print("✅ WHATSAPP: Webdriver-Manager iniciou o chromedriver.")
        except Exception as e_driver:
            print(f"!!! WHATSAPP: Falha ao iniciar o ChromeDriverManager: {e_driver}")
            return False

        driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            "platformOverride": "Win32",
            "userAgentMetadata": {
                "platform": "Windows",
                "platformVersion": "10.0",
                "architecture": "x86",
                "model": "",
                "mobile": False
            }
        })
        driver.execute_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
            Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
            Object.defineProperty(navigator, 'languages', { get: () => ['pt-BR', 'pt', 'en-US', 'en'] });
        """)

        driver.set_page_load_timeout(90)
        wait = WebDriverWait(driver, 60) 
        
        print("... WHATSAPP: Abrindo WhatsApp Web...")
        driver.get("https://web.whatsapp.com/")

        time.sleep(random.uniform(10.0, 15.0))
        
        print(f"... WHATSAPP: Buscando campo de busca...")
        search_box_xpath = "//div[@contenteditable='true']"
        try:
            search_box = wait.until(EC.visibility_of_element_located((By.XPATH, search_box_xpath)))
        except TimeoutException:
            print("❌ Campo de busca não encontrado")
            return False
        
        time.sleep(random.uniform(3.0, 4.0))
        
        search_box.click()
        search_box.clear()
        search_box.send_keys(NOME_EXATO_DO_GRUPO_WHATSAPP)
        time.sleep(random.uniform(4.0, 6.0))
        
        group_found = False
        try:
            group_items = driver.find_elements(By.XPATH, f"//span[@title]")
            for item in group_items:
                title = item.get_attribute('title')
                if title and title.strip() == NOME_EXATO_DO_GRUPO_WHATSAPP:
                    try:
                        driver.execute_script("arguments[0].scrollIntoView(true);", item)
                        time.sleep(0.5)
                        item.click()
                    except:
                        parent = item.find_element(By.XPATH, "./ancestor::div[@role='button' or @role='link'][1]")
                        parent.click()
                    group_found = True
                    break
        except Exception:
            pass
        
        if not group_found:
            print(f"❌ Não consegui encontrar o grupo '{NOME_EXATO_DO_GRUPO_WHATSAPP}'")
            return False
        
        time.sleep(random.uniform(5.0, 7.0))
        
        try:
            chat_title = wait.until(EC.presence_of_element_located((By.XPATH, f"//span[@title='{NOME_EXATO_DO_GRUPO_WHATSAPP}']")))
            print("✅ Entrou no chat do grupo.")
        except:
            print("❌ Erro ao verificar entrada no chat.")
            return False

        print("... WHATSAPP: Anexando imagem com PyAutoGUI (Colar + Foco)...")
        
        attach_button = None
        try:
            buttons = driver.find_elements(By.XPATH, "//footer//div[@role='button']")
            if buttons:
                attach_button = buttons[0]
                attach_button.click()
                time.sleep(random.uniform(2.0, 3.0))
        except:
            print("⚠️ Falha ao clicar no botão de anexo (clips).")
            return False
        
        fotos_videos_clicked = False
        try:
            fotos_videos_elem = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Fotos e vídeos')]"))
            )
            fotos_videos_elem.click()
            print("✅ WHATSAPP: Clicou em 'Fotos e vídeos'. Janela nativa deve estar aberta.")
            fotos_videos_clicked = True
            time.sleep(random.uniform(5.0, 7.0))
        except:
            print("⚠️ WHATSAPP: 'Fotos e vídeos' não encontrado. Não foi possível abrir a janela nativa.")
        
        if not fotos_videos_clicked:
            print("!!! WHATSAPP: Falha ao iniciar o diálogo de seleção de arquivos. Abortando upload.")
        else:
            try:
                print(f"📁 Caminho: {temp_image_path}")
                pyperclip.copy(temp_image_path)
                
                pyautogui.hotkey('alt', 'd')
                time.sleep(random.uniform(1.0, 1.5))
                
                pyautogui.hotkey('ctrl', 'v')
                print("✅ PyAutoGUI: Caminho do arquivo COLADO.")
                
                time.sleep(random.uniform(2.0, 3.0))
                
                pyautogui.press('enter')
                print("✅ PyAutoGUI: ENTER pressionado. Upload iniciado.")
                
                time.sleep(random.uniform(5.0, 7.0))
                
                print("✅ WHATSAPP: Imagem enviada para pré-visualização com sucesso.")
                
                print("... WHATSAPP: Procurando campo de legenda...")
                msg_input = None
                
                short_wait = WebDriverWait(driver, 15)
                
                try:
                    msg_input = short_wait.until(
                        EC.element_to_be_clickable((By.XPATH, "//div[@contenteditable='true'][@role='textbox']"))
                    )
                    
                    if not msg_input:
                        msg_inputs = driver.find_elements(By.XPATH, "//div[@contenteditable='true']")
                        if msg_inputs:
                            msg_input = msg_inputs[-1]
                    
                    print("      ✅ Campo de legenda encontrado!")
                except:
                    pass
                
                if msg_input:
                    try:
                        msg_input.click()
                        time.sleep(random.uniform(1.0, 2.0))
                        
                        print("... WHATSAPP: Copiando mensagem para clipboard...")
                        pyperclip.copy(mensagem_whatsapp)
                        msg_input.send_keys(Keys.CONTROL + 'v')
                        print("✅ WHATSAPP: Legenda colada via clipboard")
                        
                        time.sleep(random.uniform(3.0, 5.0)) 
                    except Exception as e:
                        print(f"!!! WHATSAPP: Erro ao digitar legenda: {str(e)[:100]}")
                        raise

                
                envio_confirmado = False
                
                try:
                    print("... WHATSAPP: [Tentativa 1] Enviando com Keys.ENTER...")
                    msg_input.send_keys(Keys.ENTER)
                    
                    print("... WHATSAPP: ENTER enviado. Aguardando caixa de legenda desaparecer (staleness)...")
                    short_wait.until(
                        EC.staleness_of(msg_input)
                    )
                    
                    print("✅ WHATSAPP: Envio confirmado via Keys.ENTER + Staleness!")
                    envio_confirmado = True
                    
                    print("... WHATSAPP: Aguardando 7 segundos extras para garantir o envio completo...")
                    time.sleep(7.0) 
                    
                except Exception as e_enter:
                    print(f"❌ Envio via ENTER falhou (Provavelmente só pulou linha). Erro: {str(e_enter)[:80]}")

                if not envio_confirmado:
                    try:
                        print("... WHATSAPP: [Tentativa 2] Enviando com CLIQUE no botão (Plano B)...")
                        
                        send_button = short_wait.until(
                            EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Enviar' and @role='button'] | //span[@data-testid='send'] | //button[@data-testid='send']"))
                        )
                        
                        driver.execute_script("arguments[0].click();", send_button)
                        
                        print("... WHATSAPP: Clique JS executado. Aguardando botão desaparecer (staleness)...")
                        short_wait.until(
                            EC.staleness_of(send_button)
                        )
                        
                        print("✅ WHATSAPP: Envio confirmado via CLIQUE + Staleness!")
                        envio_confirmado = True
                        
                        print("... WHATSAPP: Aguardando 7 segundos extras para garantir o envio completo...")
                        time.sleep(7.0) 
                        
                    except Exception as e_click:
                        print(f"❌ Envio via CLIQUE também falhou. Erro: {str(e_click)[:80]}")

                
                if not envio_confirmado:
                    print("!!! WHATSAPP: Falha ao confirmar o envio (Nem Enter, nem Clique).")
                    raise WebDriverException("Envio não confirmado.")

                envio_status = True
                
            except Exception as e:
                print(f"!!! ERRO CRÍTICO no bloco PyAutoGUI/Envio: {str(e)[:150]}")
                envio_status = False
            
    except Exception as e:
        print(f"!!! WHATSAPP: Erro geral: {str(e)[:150]}")
        envio_status = False
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass
        
        if temp_image_path and os.path.exists(temp_image_path):
            try:
                os.remove(temp_image_path)
                print(f"🗑️ Arquivo temporário removido: {temp_image_path}")
            except:
                pass
    
    print(f"--- WHATSAPP: Envio {'SUCESSO' if envio_status else 'FALHOU'}! ---")
    return envio_status

async def enviar_promocao(bot, produto_info, share_info):
    item_id = produto_info['item_id']
    titulo = produto_info['titulo'] 
    imagem_url = produto_info['imagem_url']
    
    titulo_formatado = formatar_titulo_com_volume(titulo)
    
    link_afiliado = share_info.get("link")
    precos_info = share_info.get("precos")
    
    cupom_info = share_info.get("cupom_info") 
    
    vendedor_info = share_info.get("vendedor_info", {})
    vendedor_nome = vendedor_info.get("nome", "Mercado Livre")
    vendedor_vendas = vendedor_info.get("vendas")
    
    if not link_afiliado or not link_afiliado.startswith("http"):
        print(f"!!! Link inválido: '{link_afiliado}'")
        return False 
    
    if link_afiliado_ja_enviado(link_afiliado):
        print(f"Link de afiliado já enviado anteriormente")
        return False 
    
    if not precos_info:
        print("!!! Preços não disponíveis")
        return False 
    
    print(f"\n[{time.strftime('%H:%M:%S')}] Formatando envio: {titulo} (Vendedor: {vendedor_nome})")
    
    mensagem_final_html = ""
    mensagem_curta_html = ""
    
    try:
        cabecalho_customizado = f"<b>✨ {titulo_formatado.upper()}</b>" 
        
        preco_atual_num = validar_preco(precos_info['preco_atual'], "preco_atual")
        if not preco_atual_num:
            print("!!! Preço atual (promocional) inválido. NÃO ENVIANDO.")
            return False 
        
        preco_original_num = validar_preco(precos_info.get('preco_original'), "preco_original")
        
        preco_final_num = preco_atual_num
        tem_cupom_auto = False
        valor_economia_cupom_num = None
        cupom_manual_code = None
        
        if cupom_info:
            valor_economia_cupom_num = cupom_info.get('valor_economia_auto')
            cupom_manual_code = cupom_info.get('codigos')
            
            if valor_economia_cupom_num and valor_economia_cupom_num < preco_atual_num:
                preco_final_num = preco_atual_num - valor_economia_cupom_num
                tem_cupom_auto = True
            else:
                print(f"      ... Nenhum desconto automático ('economiza R$') encontrado no Iframe.")
        
        preco_final_num = max(0.01, preco_final_num)
        
        preco_str = ""
        economia_str = ""
        
        preco_de = None
        if preco_original_num and preco_original_num > preco_atual_num:
            preco_de = preco_original_num
        elif tem_cupom_auto and preco_atual_num > preco_final_num:
            preco_de = preco_atual_num
        elif preco_original_num:
            preco_de = preco_original_num
        
        preco_a_pagar = preco_final_num if tem_cupom_auto else preco_atual_num

        is_pix_price = precos_info.get('is_pix_price', False)
        pix_str = " <b>no Pix</b>" if is_pix_price else ""

        if preco_de:
            preco_str = f"❌ De: <s>R$ {preco_de:.2f}</s>\n"
        
        if preco_de and preco_de > preco_atual_num and tem_cupom_auto:
            desc_promo_percent, _ = calcular_desconto_seguro(preco_de, preco_atual_num)
            promo_percent_str = f" ({desc_promo_percent}% OFF)" if desc_promo_percent else ""
            preco_str += f"🔥 <b>Promoção: R$ {preco_atual_num:.2f}</b>{pix_str}\n"

        elif preco_de and preco_de > preco_atual_num and not tem_cupom_auto:
            preco_str += f"🔥 <b>Por: R$ {preco_atual_num:.2f}</b>{pix_str}\n"
        
        if tem_cupom_auto:
            preco_str += f"💲 <b>Desconto CUPOM: -R$ {valor_economia_cupom_num:.2f}</b>\n"
                            
        if preco_de and preco_de > preco_a_pagar:
            economia_total = preco_de - preco_a_pagar
            if economia_total > 0.01:
                percentual_total = int((economia_total / preco_de) * 100)
                economia_str = f"🤯 <b>Desconto TOTAL: R$ {economia_total:.2f} ({percentual_total}% OFF)</b>"
        
        preco_str += economia_str

        if tem_cupom_auto:
            padding_central = " " * 3 
            preco_str += f"\n\n{padding_central}✅ <b><u>PREÇO FINAL: R$ {preco_a_pagar:.2f}</u></b> ✅"
                            
        elif not preco_de:
            preco_str = f"🛒 <b>Preço:</b> R$ {preco_atual_num:.2f}{pix_str}"
            
        elif preco_de == preco_atual_num and not tem_cupom_auto:
            preco_str = f"🛒 <b>Preço:</b> R$ {preco_atual_num:.2f}{pix_str}"
            
        elif not preco_str:
            preco_str = f"🛒 <b>Preço:</b> R$ {preco_a_pagar:.2f}{pix_str}"

        manual_cupom_str = ""
        if cupom_manual_code:
            print(f"      ... Códigos manuais encontrados: {cupom_manual_code}")
            manual_cupom_str = (
                f"\n\n🎟️ <b>CUPONS:</b> <code>{cupom_manual_code}</code>\n"
                f"<i>(Copie e cole no carrinho!)</i>"
            )
        
        loja_str = f"🏪 <b>Loja:</b> {vendedor_nome}\n"
        
        if vendedor_vendas:
            loja_str += f"📦 <b>Vendas: {vendedor_vendas}</b>\n"
        
        mensagem_final_html = (
            f"{cabecalho_customizado}\n\n" 
            f"{preco_str}"
            f"{manual_cupom_str}\n\n"
            f"{loja_str.strip()}"   
            f"\n\n🔗 <b>COMPRAR AGORA:</b> {link_afiliado}"
        )
        
        await bot.send_photo(
            chat_id=TELEGRAM_GROUP_ID,
            photo=imagem_url,
            caption=mensagem_final_html,
            parse_mode="HTML"
        )
        
        print(f"✅ SUCESSO! {titulo} (Enviado para o Telegram)")
        salvar_link_afiliado(link_afiliado)
        
        print(f"---[{time.strftime('%H:%M:%S')}] Iniciando envio para o WhatsApp em background...")
        loop = asyncio.get_running_loop()
        
        await loop.run_in_executor(
            None, 
            enviar_para_whatsapp, 
            mensagem_final_html,
            imagem_url      
        )
        
        return True 
        
    except Exception as e:
        if "message is too long" in str(e):
            print("!!! Mensagem longa, reenviando versão curta...")
            try:
                loja_str = f"🏪 {vendedor_nome}\n"
                if vendedor_vendas: 
                    loja_str += f"🏅 Vendas Loja: {vendedor_vendas}\n"

                mensagem_curta_html = (
                    f"<b>✨ {titulo_formatado.upper()}</b>\n\n" 
                    f"{preco_str}" 
                    f"{manual_cupom_str}\n\n"
                    f"{loja_str.strip()}"
                    f"\n\n🔗 COMPRAR: {link_afiliado}"
                )
                
                await bot.send_photo(
                    chat_id=TELEGRAM_GROUP_ID,
                    photo=imagem_url,
                    caption=mensagem_curta_html,
                    parse_mode="HTML"
                )
                
                print(f"✅ SUCESSO (versão curta)! {titulo}")
                salvar_link_afiliado(link_afiliado)
                
                loop = asyncio.get_running_loop()
                await loop.run_in_executor(
                    None,
                    enviar_para_whatsapp,
                    mensagem_curta_html,
                    imagem_url
                )
                
                return True 
            except Exception as e2:
                print(f"!!! Erro mesmo com versão curta: {e2}")
                return False 
        else:
            print(f"!!! Erro no envio (Telegram ou WhatsApp): {e}")
            return False 


# --- BLOCO 5: LÓGICA PRINCIPAL (BUSCA E LOOP) ---

async def construir_grupos_de_produtos_ml(modelos_falhados_a_ignorar: set):
    global grupos_de_produtos, modelos_ja_enviados_historico, URLS_BUSCA_ML, titulos_encontrados_neste_scan
    
    grupos_de_produtos.clear()
    
    print(f"\n[{time.strftime('%H:%M:%S')}] 🔄 Iniciando scan de {len(URLS_BUSCA_ML)} marcas árabes...")
    print(f"    (Ignorando {len(modelos_ja_enviados_historico)} modelos permanentes e {len(modelos_falhados_a_ignorar)} temporários)")
    
    if not modelos_falhados_a_ignorar:
        titulos_encontrados_neste_scan.clear() 
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    total_modelos_unicos_neste_scan = 0
    
    for page_counter, url in enumerate(URLS_BUSCA_ML, 1):
        marca_nome = list(MARCAS_ARABES.keys())[page_counter - 1] if page_counter <= len(MARCAS_ARABES) else "Desconhecida"
        produtos_encontrados_nesta_pagina = 0
            
        try:
            print(f"    [Sync] Buscando marca {page_counter}/{len(URLS_BUSCA_ML)}: {marca_nome}...")
            response = requests.get(url, headers=headers, timeout=20)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            cards = soup.find_all('div', class_='andes-card--flat')
            
            if not cards or len(cards) < 2:
                cards = soup.find_all('li', class_='ui-search-layout__item')
                if not cards:
                    continue
            
            if cards and 'andes-card--flat' in str(cards[0]):
                produtos = cards[1:]
            else:
                produtos = cards
            
            if not produtos:
                continue
                
            for item in produtos:
                link_tag = None
                titulo = None
                img_tag = None
                
                if item.find('a', class_='poly-component__title'):
                    link_tag = item.find('a', class_='poly-component__title')
                    if link_tag:
                        titulo = link_tag.text.strip()
                    img_tag = item.find('img', class_='poly-component__picture')
                
                else:
                    titulo_tag = item.find('h2', class_='ui-search-item__title')
                    link_tag = item.find('a', class_='ui-search-link')
                    # --- [CORREÇÃO DE SINTAXE v57.1] ---
                    # Corrigido de class= para class_=
                    img_tag = item.find('img', class_='ui-search-result-image__element')
                    
                    if titulo_tag:
                        titulo = titulo_tag.text.strip()
                
                if not (titulo and link_tag and img_tag):
                    continue 
                
                if not modelos_falhados_a_ignorar:
                    titulos_encontrados_neste_scan.append(titulo) 
                
                titulo_lower = titulo.lower()
                if any(palavra in titulo_lower for palavra in PALAVRAS_EXCLUIDAS):
                    continue
                
                preco_lista_num = None
                for selector in SELECTORS_ML["list_price_fraction"]:
                    try:
                        price_elem = item.select_one(selector)
                        if price_elem:
                            preco_lista_num = validar_preco(price_elem.text, "preco_lista")
                            if preco_lista_num:
                                break
                    except Exception:
                        continue
                
                if not preco_lista_num:
                    continue
                
                hash_key, volume_ml_int = gerar_hash_inteligente(titulo)
                if not hash_key or not volume_ml_int:
                    continue
                
                if volume_ml_int < 49:
                    continue
                    
                if hash_key in modelos_ja_enviados_historico:
                    continue 
                
                if hash_key in modelos_falhados_a_ignorar:
                    continue

                base_url = "https://www.mercadolivre.com.br"
                link_href = link_tag.get('href')
                if not link_href:
                    continue
                link_original = urllib.parse.urljoin(base_url, link_href)
                
                imagem_url = img_tag.get('data-src', img_tag.get('src'))
                if not imagem_url or imagem_url.startswith("data:image"):
                    imagem_url = "https://http2.mlstatic.com/static/org-img/homesnw/mercado-libre.png" 
                if imagem_url and not imagem_url.startswith("https://"):
                    imagem_url = "https://" + imagem_url.lstrip(':').lstrip('/')
                
                mlb_id = extrair_mlb_id(link_original)
                hash_titulo_simples = gerar_hash_titulo(titulo)
                
                if mlb_id and hash_titulo_simples:
                    item_id = f"{mlb_id}*{hash_titulo_simples}"
                else:
                    item_id = "ML_" + link_original.split('/')[-1][:20]
                
                produto_bruto = {
                    "item_id": item_id,
                    "hash_key": hash_key,
                    "titulo": titulo,
                    "link_original": link_original,
                    "imagem_url": imagem_url,
                    "preco_lista": preco_lista_num, 
                    "tags_str": "", 
                    "source": "Mercado Livre",
                    "marca": marca_nome
                }
                
                if hash_key not in grupos_de_produtos:
                        grupos_de_produtos[hash_key] = []
                        total_modelos_unicos_neste_scan += 1
                grupos_de_produtos[hash_key].append(produto_bruto)
                produtos_encontrados_nesta_pagina += 1
            
            sleep_time = random.uniform(DELAY_SCAN_PAGINA_MIN, DELAY_SCAN_PAGINA_MAX)
            time.sleep(sleep_time) 
            
        except Exception as e_page:
            print(f"!!! ERRO ao processar marca {marca_nome} ({url}): {e_page}")
            print(f"    Continuando para a próxima marca...")
            continue
    
    print(f"\n✅ Scan de {len(URLS_BUSCA_ML)} marcas árabes concluído.")
    print(f"    Modelos únicos encontrados *neste scan*: {total_modelos_unicos_neste_scan}")
    return total_modelos_unicos_neste_scan


# --- BLOCO 5.5: GERADOR DE RELATÓRIO ---

async def gerar_relatorio_grupos():
    global grupos_de_produtos
    
    print(f"📄 Gerando relatório para {len(grupos_de_produtos)} grupos...")
    
    try:
        with open(ARQUIVO_RELATORIO_GRUPOS, 'w', encoding='utf-8') as f:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"--- RELATÓRIO DE GRUPOS GERADO EM: {timestamp} ---\n")
            f.write(f"Total de Modelos Únicos Encontrados: {len(grupos_de_produtos)}\n")
            f.write("--------------------------------------------------\n\n")
            
            sorted_hash_keys = sorted(grupos_de_produtos.keys())
            
            for i, hash_key in enumerate(sorted_hash_keys, 1):
                anuncios = grupos_de_produtos[hash_key]
                
                precos = [p.get('preco_lista', 0) for p in anuncios]
                precos.sort()
                precos_formatados = [f"R$ {p:.2f}" for p in precos]
                
                f.write(f"GRUPO {i}: {hash_key}\n")
                f.write(f"  - Anúncios Encontrados: {len(anuncios)}\n")
                f.write(f"  - Preços: {', '.join(precos_formatados)}\n")
                f.write(f"  - Mais Barato: {precos_formatados[0]}\n\n")
        
        print(f"✅ Relatório salvo em: {ARQUIVO_RELATORIO_GRUPOS}")
        
    except Exception as e:
        print(f"!!! ERRO ao gerar relatório de grupos: {e}")

async def gerar_relatorio_titulos():
    global titulos_encontrados_neste_scan
    
    if not titulos_encontrados_neste_scan:
        print("📄 Relatório de Títulos Brutos pulado (nenhum título novo no scan).")
        return
        
    print(f"📄 Gerando relatório de Títulos Brutos ({len(titulos_encontrados_neste_scan)})...")
    
    try:
        with open(ARQUIVO_RELATORIO_TITULOS, 'w', encoding='utf-8') as f:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"--- RELATÓRIO DE TÍTULOS GERADO EM: {timestamp} ---\n")
            f.write(f"Total de Títulos Brutos Coletados: {len(titulos_encontrados_neste_scan)}\n")
            f.write("--------------------------------------------------\n\n")
            
            for titulo in titulos_encontrados_neste_scan:
                f.write(f"{titulo}\n")
        
        print(f"✅ Relatório de Títulos salvo em: {ARQUIVO_RELATORIO_TITULOS}")
        
    except Exception as e:
        print(f"!!! ERRO ao gerar relatório de títulos: {e}")

# --- [REMOVIDO v56] ---
# A função 'proxima_marca_com_anuncios' foi removida.
# A lógica de rotação agora é aleatória e tratada no loop 'main'.
# def proxima_marca_com_anuncios(marca_atual_index, grupos):
#    ... (código antigo removido) ...

async def main():
    global modelos_ja_enviados_historico, grupos_de_produtos, historico_de_precos
    
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    # --- [MUDANÇA v57.1] ---
    print("🤖 Bot v57.1 (Fix 'Preço DE' + Fix SyntaxError) iniciado!")
    
    try:
        with open(ARQUIVO_HISTORICO, 'r', encoding='utf-8') as f:
            modelos_ja_enviados_historico = set(line.strip() for line in f)
            print(f"📋 Histórico de MODELOS carregado: {len(modelos_ja_enviados_historico)} modelos")
    except FileNotFoundError:
        print(f"📋 Histórico de MODELOS não encontrado, começando do zero")
        modelos_ja_enviados_historico = set()
    except Exception as e:
        print(f"⚠️ Erro ao carregar histórico de MODELOS: {e}")
        modelos_ja_enviados_historico = set()
    
    carregar_historico_precos()
    
    intervalo_novo_ciclo_seg = EMPTY_QUEUE_WAIT_MINUTES * 60
    
    while True:
        
        modelos_falhados_neste_ciclo_atual = set() 
        
        print(f"\n--- INICIANDO NOVO CICLO [{time.strftime('%H:%M:%S')}] ---")
        
        houve_envio_neste_ciclo_completo = False
        
        while True:
            
            total_modelos_encontrados = await construir_grupos_de_produtos_ml(
                modelos_falhados_neste_ciclo_atual
            )
            
            await gerar_relatorio_grupos()
            await gerar_relatorio_titulos()
            
            if not grupos_de_produtos or total_modelos_encontrados == 0:
                print(f"[{time.strftime('%H:%M:%S')}] Nenhum novo grupo de produto encontrado no scan.")
                break
            
            # --- [INÍCIO DA LÓGICA DE ROTAÇÃO ALEATÓRIA v56] ---
            # Substitui o 'proxima_marca_com_anuncios' e 'marca_index_atual'
            
            print(f"Processando {len(grupos_de_produtos)} modelos únicos com ROTAÇÃO ALEATÓRIA de marcas...")
            
            contador_envios_neste_lote = 0
            
            # 1. Pega todas as marcas que TÊM produtos na fila
            marcas_com_produtos = set()
            for hash_key in grupos_de_produtos:
                for anuncio in grupos_de_produtos[hash_key]:
                    # Garante que 'marca' não é None
                    marca_anuncio = anuncio.get('marca')
                    if marca_anuncio:
                        marcas_com_produtos.add(marca_anuncio)
            
            if not marcas_com_produtos:
                print("... Nenhuma marca com produtos encontrados. Quebrando o ciclo.")
                break
                
            # 2. Cria uma lista aleatória de marcas para processar
            marcas_para_processar = list(marcas_com_produtos)
            random.shuffle(marcas_para_processar)
            
            print(f"    Marcas na fila de rotação: {marcas_para_processar}")
            
            marcas_iter = iter(marcas_para_processar)
            
            # --- [FIM DA LÓGICA DE ROTAÇÃO ALEATÓRIA v56] ---

            while contador_envios_neste_lote < 5:
                
                # --- [SUBSTITUIÇÃO DE 'proxima_marca_com_anuncios'] ---
                try:
                    marca_nome = next(marcas_iter)
                except StopIteration:
                    print(f"[{time.strftime('%H:%M:%S')}] Fim da rotação de marcas. Enviados {contador_envios_neste_lote} produtos.")
                    break # Sai do loop de 5 envios
                # --- [FIM DA SUBSTITUIÇÃO] ---
                
                print(f"\n▶️  ALTERNANDO para marca (Aleatória): {marca_nome}")
                
                # Encontra primeiro anúncio desta marca que não foi enviado
                anuncio_encontrado = None
                hash_key_encontrado = None
                
                for hash_key in list(grupos_de_produtos.keys()):
                    anuncios_do_modelo = grupos_de_produtos[hash_key]
                    
                    # Filtra anúncios apenas da marca atual
                    anuncios_da_marca_neste_modelo = [
                        a for a in anuncios_do_modelo 
                        if a.get('marca') == marca_nome
                    ]
                    
                    if not anuncios_da_marca_neste_modelo:
                        continue
                    
                    # Ordena por preço (mais barato primeiro)
                    anuncios_da_marca_neste_modelo.sort(key=lambda p: p.get('preco_lista', 99999))
                    
                    # Pega o mais barato desta marca/modelo
                    anuncio_encontrado = anuncios_da_marca_neste_modelo[0]
                    hash_key_encontrado = hash_key
                    break
                
                if not anuncio_encontrado:
                    print(f"    ❌ Nenhum anúncio disponível da marca {marca_nome} neste momento.")
                    continue
                
                preco_lista_num = anuncio_encontrado.get('preco_lista')
                item_id = anuncio_encontrado['item_id']
                titulo = anuncio_encontrado['titulo']
                link_original = anuncio_encontrado['link_original']
                
                print(f"    -> [MARCA: {marca_nome}] Tentando Anúncio (ID: {item_id[-10:]}): R$ {preco_lista_num} - {titulo[:30]}...")

                if not validar_promocao(hash_key_encontrado, preco_lista_num):
                    print(f"    -> 🚫 PREÇO RUIM (R$ {preco_lista_num} > média). Descartando anúncio.")
                    salvar_historico_precos(hash_key_encontrado, preco_lista_num, link_original)
                    # Remove este anúncio da lista
                    grupos_de_produtos[hash_key_encontrado].remove(anuncio_encontrado)
                    continue
                
                print("    -> ✅ Preço OK.")
                
                share_info = get_share_link_and_seller(anuncio_encontrado)
                
                if share_info is None:
                    print(f"    -> 🚫 SELENIUM FALHOU (Página não carregou ou erro). Descartando anúncio.")
                    logar_erro(item_id, titulo, link_original, "get_share_link_and_seller retornou None")
                    grupos_de_produtos[hash_key_encontrado].remove(anuncio_encontrado)
                    continue
                    
                vendedor_info = share_info.get("vendedor_info", {})
                vendas_str = vendedor_info.get("vendas")
                vendas_int = normalizar_contagem_vendas(vendas_str)
                
                if vendas_int is not None and vendas_int < MINIMO_VENDAS_VENDEDOR:
                    print(f"    -> 🚫 VENDEDOR FRACO ({vendas_int} vendas). Descartando anúncio.")
                    logar_erro(item_id, titulo, link_original, f"Vendedor Fraco ({vendas_int} vendas)", share_info)
                    grupos_de_produtos[hash_key_encontrado].remove(anuncio_encontrado)
                    continue
                elif vendas_int is None:
                    print(f"    -> ⚠️ Vendas não encontradas. Permitindo...")
                else:
                    print(f"    -> ✅ Vendedor OK ({vendas_int} vendas).")

                foi_enviado = await enviar_promocao(bot, anuncio_encontrado, share_info)
                
                if foi_enviado:
                    print(f"    -> ✅ SUCESSO! Modelo {hash_key_encontrado} enviado da marca {marca_nome}.")
                    contador_envios_neste_lote += 1
                    houve_envio_neste_ciclo_completo = True
                    
                    modelos_ja_enviados_historico.add(hash_key_encontrado)
                    salvar_no_historico(hash_key_encontrado) 
                    
                    preco_real_selenium = validar_preco(share_info.get('precos', {}).get('preco_atual'))
                    if preco_real_selenium:
                         salvar_historico_precos(hash_key_encontrado, preco_real_selenium, share_info.get('link'))
                    
                    # Remove este anúncio após envio bem-sucedido
                    grupos_de_produtos[hash_key_encontrado].remove(anuncio_encontrado)
                    
                    min_segundos = SEND_INTERVAL_MIN_MINUTES * 60
                    max_segundos = SEND_INTERVAL_MAX_MINUTES * 60
                    delay_aleatorio_segundos = random.uniform(min_segundos, max_segundos)
                    
                    print(f"    [DELAY] Envio OK. Aguardando {delay_aleatorio_segundos / 60:.1f} min antes de continuar...")
                    await asyncio.sleep(delay_aleatorio_segundos)
                else:
                    print("    -> 🚫 FALHA NO ENVIO (Telegram/WhatsApp). Descartando anúncio.")
                    logar_erro(item_id, titulo, link_original, "enviar_promocao retornou False", share_info)
                    grupos_de_produtos[hash_key_encontrado].remove(anuncio_encontrado)
                
                await asyncio.sleep(random.uniform(2.0, 5.0))
            
            # Após 5 envios ou fim da rotação, força novo scan
            print(f"\n--- [LOTE DE {contador_envios_neste_lote} ENVIADO] ---")
            print(f"Forçando re-scan para atualizar os preços...")
            
            grupos_de_produtos.clear()
            
            if contador_envios_neste_lote < 5:
                print(f"[{time.strftime('%H:%M:%S')}] Fim do lote (enviou {contador_envios_neste_lote} produtos).")
                break

        if not houve_envio_neste_ciclo_completo:
            print(f"\n[{time.strftime('%H:%M:%S')}] Ciclo de processamento concluído. Nenhum novo produto enviado.")
            print(f"Aguardando {EMPTY_QUEUE_WAIT_MINUTES} min para o próximo ciclo de busca...")
            await asyncio.sleep(intervalo_novo_ciclo_seg)


# --- BLOCO 6: PONTO DE ENTRADA ---

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Bot desligado manualmente (KeyboardInterrupt)")
    except Exception as e:
        print(f"\n!!! ERRO CRÍTICO no loop principal: {e}")
        time.sleep(2)