# Comando para criar um Serviço de Backend (Backend Service)

## Descrição

O comando `create` inicializa um serviço de backend, que é um recurso central para o Cloud Load Balancing. Ele define como o tráfego é distribuído para um ou mais grupos de instâncias (backends) associados. Um serviço de backend precisa ser configurado com informações cruciais como o protocolo de comunicação e uma verificação de saúde (health check) para monitorar a disponibilidade dos backends.

Após a criação, você deve adicionar um ou mais backends (ex: grupos de instâncias) a ele.

### Comando básico para criar um Serviço de Backend HTTP

```bash
gcloud compute backend-services create meu-backend-http \
    --protocol HTTP \
    --health-checks meu-health-check-http \
    --global \
    --description="Serviço de backend para o frontend web"
```

Este comando cria um serviço de backend global, ideal para um Load Balancer de HTTP(S) Externo. Ele ainda não possui backends.

### Adicionando um Backend (Passo Essencial)

Após criar o serviço, você precisa associar um grupo de instâncias a ele.

```bash
gcloud compute backend-services add-backend meu-backend-http \
    --instance-group=meu-grupo-de-instancias \
    --instance-group-zone=us-central1-a \
    --global
```

Este segundo comando vincula o `meu-grupo-de-instancias` ao serviço de backend recém-criado, permitindo que ele receba tráfego.

## Saída esperada (do comando `create`)

```json
{
  "affinityCookieTtlSec": 0,
  "creationTimestamp": "2025-07-04T12:20:00.123-03:00",
  "description": "Serviço de backend para o frontend web",
  "enableCDN": false,
  "fingerprint": "AbCdEfGhIjK=",
  "healthChecks": [
    "https://www.googleapis.com/compute/v1/projects/meu-projeto/global/healthChecks/meu-health-check-http"
  ],
  "id": "1234567890123456789",
  "kind": "compute#backendService",
  "loadBalancingScheme": "EXTERNAL",
  "name": "meu-backend-http",
  "port": 80,
  "portName": "http",
  "protocol": "HTTP",
  "selfLink": "https://www.googleapis.com/compute/v1/projects/meu-projeto/global/backendServices/meu-backend-http",
  "sessionAffinity": "NONE",
  "timeoutSec": 30
}
```

## Opções principais

  * `--protocol`: Protocolo usado para comunicar com os backends. (Ex: `HTTP`, `HTTPS`, `HTTP2`, `TCP`, `SSL`).
  * `--health-checks`: Uma ou mais verificações de saúde (health checks) para determinar a disponibilidade dos backends.
  * `--description`: Uma descrição textual para o serviço de backend.
  * `--load-balancing-scheme`: Define o tipo de load balancer. Valores comuns são `EXTERNAL` para tráfego da internet e `INTERNAL_MANAGED` para tráfego interno.
  * `--port-name`: Um nome para a porta na qual o serviço operará. Ex: `http` (que mapeia para a porta 80).
  * `--global` ou `--region`: Define o escopo do serviço. Use `--global` para load balancers globais (como HTTP/S) e `--region` para regionais.