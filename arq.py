import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import schedule
import time
import matplotlib.pyplot as plt

# Função para ler dados do arquivo CSV
def ler_dados_csv(nome_arquivo):
    try:
        # Lê o arquivo CSV com ponto e vírgula como delimitador
        df = pd.read_csv(nome_arquivo, delimiter=';')
        # Remove as linhas que contêm valores nulos em 'Nome' ou 'Cpf' ou 'Data'
        df = df.dropna(subset=['Nome', 'Cpf', 'Data'])
        return df[['Nome', 'Cpf', 'Data']]  # Seleciona apenas as colunas 'Nome', 'Cpf' e 'Data'
    except FileNotFoundError:
        print(f"Arquivo {nome_arquivo} não encontrado.")
        return pd.DataFrame()

# Função para enviar e-mail com dashboard
def enviar_email(dados):
    seu_email = 'rayanvictor088@gmail.com'
    sua_senha = 'pebe drim wjeu ydcq'

    destinatario = 'alicebarbosaaraujo5@gmail.com'
    assunto = 'Dados do Arquivo CSV com Dashboard'

    # Criar gráfico de barras
    plt.figure(figsize=(8, 6))
    dados.plot(kind='bar', x='Nome', y='Cpf', legend=False)
    plt.title('Gráfico de Barras - CPF por Nome')
    plt.xlabel('Nome')
    plt.ylabel('CPF')
    plt.tight_layout()
    plt.savefig('dashboard.png')  # Salvar o gráfico como uma imagem

    # Construir corpo do e-mail
    corpo_email = MIMEMultipart()
    corpo_email.attach(MIMEText(dados.to_string(), 'plain'))

    # Adicionar imagem ao e-mail como anexo
    with open('dashboard.png', 'rb') as img:
        imagem = MIMEBase('application', 'octet-stream')
        imagem.set_payload(img.read())
        encoders.encode_base64(imagem)
        imagem.add_header('Content-Disposition', 'attachment; filename="dashboard.png"')
        corpo_email.attach(imagem)

    mensagem = MIMEMultipart()
    mensagem.attach(corpo_email)
    mensagem['Subject'] = assunto
    mensagem['From'] = seu_email
    mensagem['To'] = destinatario

    # Conectar ao servidor SMTP
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(seu_email, sua_senha)

    # Enviar e-mail
    server.sendmail(seu_email, destinatario, mensagem.as_string())

    # Fechar a conexão
    server.quit()

# Função para agendar o envio de e-mail
def agendar_envio():
    nome_arquivo_csv = 'dados.csv'
    dados_do_arquivo = ler_dados_csv(nome_arquivo_csv)

    print("dados enviados")

    enviar_email(dados_do_arquivo)

    # Após o envio do e-mail, encerra o script
    exit()

# Agende o envio para 20:18
schedule.every().day.at("20:23").do(agendar_envio)

# Mantenha o script em execução para que o agendamento funcione
while True:
    schedule.run_pending()
    time.sleep(1)
