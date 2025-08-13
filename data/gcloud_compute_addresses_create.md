# Comando para criar um Proxy HTTP de Destino (Target HTTP Proxy)

## Descrição

Este comando cria um Proxy HTTP de Destino, uma parte essencial do Load Balancer de Aplicativo Externo (HTTP/S) do Google Cloud. A função deste proxy é receber tráfego HTTP de uma Regra de Encaminhamento (Forwarding Rule) e usar um Mapa de URLs (URL Map) para determinar para qual serviço de backend a requisição deve ser enviada.

Para tráfego HTTPS, utiliza-se o comando análogo `gcloud compute target-https-proxies create`, que adicionalmente requer a associação de um certificado SSL.

### Comando para criar um Proxy HTTP de Destino

O comando é direto: ele precisa de um nome e do Mapa de URLs que ele deve consultar.

```bash
gcloud compute target-http-proxies create meu-proxy-http \
    --url-map=meu-mapa-de-urls \
    --description="Proxy para rotear tráfego para o mapa principal" \
    --global
```

### Contexto: Onde este comando se encaixa?

A criação de um proxy é um dos últimos passos na configuração de um Load Balancer HTTP(S). A ordem típica é:

1.  Criar uma Verificação de Saúde (`health-checks create`).
2.  Criar um Serviço de Backend (`backend-services create`) e associar a verificação de saúde a ele.
3.  Criar um Mapa de URLs (`url-maps create`) e associar o serviço de backend a ele.
4.  **Criar o Proxy de Destino (`target-http-proxies create`) e associar o mapa de URLs a ele (este comando).**
5.  Criar uma Regra de Encaminhamento (`forwarding-rules create`) para direcionar o tráfego externo para este proxy.

## Saída esperada

```json
{
  "creationTimestamp": "2025-07-04T09:26:10.123-03:00",
  "description": "Proxy para rotear tráfego para o mapa principal",
  "id": "1234567890123456789",
  "kind": "compute#targetHttpProxy",
  "name": "meu-proxy-http",
  "selfLink": "https://www.googleapis.com/compute/v1/projects/meu-projeto/global/targetHttpProxies/meu-proxy-http",
  "urlMap": "https://www.googleapis.com/compute/v1/projects/meu-projeto/global/urlMaps/meu-mapa-de-urls"
}
```

## Opções principais

  * `--url-map`: **(Obrigatório)** O nome do Mapa de URLs que este proxy utilizará para rotear o tráfego.
  * `--description`: Uma descrição textual para o proxy.
  * `--global` ou `--region`: Define o escopo do proxy. Deve corresponder ao escopo do Mapa de URLs associado. Use `--global` para a maioria dos Load Balancers de Aplicativo Externo.