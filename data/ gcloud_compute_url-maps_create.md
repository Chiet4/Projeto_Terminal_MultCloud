# Comando para criar um Mapa de URLs (URL Map)

## Descrição

Este comando cria um Mapa de URLs, que é o cérebro de um Load Balancer HTTP(S) no GCP. Ele define as regras de roteamento que direcionam as requisições dos usuários para diferentes serviços de backend com base no nome do host e no caminho da URL solicitada.

A criação de um mapa de URLs requer, no mínimo, a definição de um serviço de backend padrão (`default service`), que receberá todo o tráfego que não corresponder a nenhuma regra específica.

### Comando Básico para criar um Mapa de URLs

Este comando cria um mapa simples que envia todo o tráfego para um único serviço de backend.

```bash
gcloud compute url-maps create meu-mapa-global \
    --default-service meu-backend-principal \
    --description "Mapa de URL para o site principal" \
    --global
```

### Exemplo de Uso (com passos seguintes)

Um mapa de URLs se torna poderoso quando você adiciona regras de caminho. O fluxo de trabalho comum é:

1.  Criar o mapa com um serviço padrão.
2.  Adicionar "matchers" de caminho para rotear URLs específicas.


````bash
# Passo 1: Criar o mapa de URL
gcloud compute url-maps create mapa-loja-virtual \
    --default-service backend-loja \
    --global

# Passo 2 (Exemplo de passo seguinte): Adicionar regras de caminho
gcloud compute url-maps add-path-matcher mapa-loja-virtual \
    --default-service backend-loja \
    --path-matcher-name api-matcher \
    --path-rules="/api/*=backend-api,/admin/*=backend-admin"
````

Neste exemplo, após a criação, adicionamos regras para que o tráfego para `/api/*` vá para o `backend-api` e `/admin/*` vá para `backend-admin`. Todo o resto continua indo para o `backend-loja`.

## Saída esperada (do comando `create`)

```json
{
  "creationTimestamp": "2025-07-04T09:21:18.123-03:00",
  "defaultService": "https://www.googleapis.com/compute/v1/projects/meu-projeto/global/backendServices/meu-backend-principal",
  "description": "Mapa de URL para o site principal",
  "fingerprint": "AbCdEfGhIjK=",
  "id": "1234567890123456789",
  "kind": "compute#urlMap",
  "name": "meu-mapa-global",
  "selfLink": "https://www.googleapis.com/compute/v1/projects/meu-projeto/global/urlMaps/meu-mapa-global"
}
```

## Opções principais

  * `--default-service`: **(Obrigatório)** O serviço de backend que receberá as requisições que não corresponderem a nenhuma regra de host ou caminho.
  * `--description`: Uma descrição textual para o mapa de URLs.
  * `--global` ou `--region`: Define o escopo do mapa. Use `--global` para Load Balancers HTTP(S) Externos Globais e `--region` para os regionais.
  * `--tests-from-file`: Permite fornecer um arquivo YAML para testar a configuração do mapa de URLs, verificando se as rotas se comportam como esperado.