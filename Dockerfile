# Usa uma imagem base com Python
FROM python:3.11-slim

# Cria um diretório dentro do container
WORKDIR /app

# Copia os arquivos
COPY . .

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta do Flask
EXPOSE 5000

# Comando de inicialização
CMD ["flask", "run"]
