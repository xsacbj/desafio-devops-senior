# Imagem de Origem
FROM node:13-alpine
WORKDIR /app

# Instalando dependências da aplicação e armazenando em cache.
COPY package.json /app/package.json
COPY package-lock.json /app/package-lock.json
RUN npm install --silent
# Copiadno arquivos da aplicação
COPY . /app

# Inicializa a aplicação
CMD ["npm", "start"]