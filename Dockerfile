# Etapa 1: Build
FROM golang:1.20-alpine AS builder

WORKDIR /app

# Copia os arquivos de dependência e baixa os módulos
COPY go.mod ./
RUN go mod download

# Copia o restante do código
COPY . .

# Compila a aplicação para um binário estático
RUN go build -o score-api .

# Etapa 2: Runtime
FROM alpine:latest

WORKDIR /app

# Copia apenas o binário gerado
COPY --from=builder /app/score-api .

# Expõe a porta que a aplicação vai usar
EXPOSE 8080

# Comando de execução
CMD ["./score-api"]
