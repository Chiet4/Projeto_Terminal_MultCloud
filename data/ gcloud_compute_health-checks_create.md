# Comando para criar uma Verificação de Saúde (Health Check)

## Descrição

Este comando cria uma Verificação de Saúde (Health Check), um recurso fundamental para garantir a resiliência de aplicações. As verificações de saúde são usadas pelo Cloud Load Balancing e por Grupos de Instâncias Gerenciados para determinar quais VMs estão aptas a receber novo tráfego ou se uma VM precisa ser recriada.

É possível criar diferentes tipos de verificações (HTTP, HTTPS, TCP, etc.), cada uma com suas próprias opções de configuração.

## Pré-requisito Essencial: Regra de Firewall
Para que qualquer verificação de saúde funcione, é obrigatório que exista uma regra de firewall permitindo o tráfego de entrada vindo dos sistemas de verificação do Google. Sem essa regra, suas instâncias sempre aparecerão como UNHEALTHY.

Certifique-se de ter uma regra que permita o tráfego dos source-ranges (35.191.0.0/16, 130.211.0.0/22, etc.) na porta que a sua verificação utiliza. Consulte a documentação de `gcloud compute firewall-rules create` para o exemplo da regra completa.

### Comando para criar uma verificação de saúde HTTP

Este é o tipo mais comum, usado para verificar se um serviço web está respondendo corretamente.

```bash
gcloud compute health-checks create http meu-health-check-basico \
    --port=80 \
    --request-path="/" \
    --description="Verifica a página inicial do servidor web" \
    --check-interval=15s \
    --timeout=5s \
    --unhealthy-threshold=3 \
    --healthy-threshold=2
```

Este comando cria uma verificação que:

  * Envia uma requisição para a porta `80` no caminho `/` a cada `15` segundos.
  * Espera no máximo `5` segundos por uma resposta.
  * Marca uma VM como "não saudável" após `3` falhas seguidas.
  * Marca uma VM como "saudável" novamente após `2` sucessos seguidos.

### Comando para criar uma verificação de saúde TCP

Uma verificação mais simples, que apenas testa se uma conexão TCP pode ser estabelecida em uma porta específica.

```bash
gcloud compute health-checks create tcp meu-health-check-ssh \
    --port=22 \
    --description="Verifica se a porta SSH está respondendo"
```

## Saída esperada (do comando HTTP)

```json
{
  "checkIntervalSec": 15,
  "creationTimestamp": "2025-07-04T09:17:00.123-03:00",
  "description": "Verifica a página inicial do servidor web",
  "healthyThreshold": 2,
  "httpHealthCheck": {
    "port": 80,
    "requestPath": "/"
  },
  "id": "1234567890123456789",
  "kind": "compute#healthCheck",
  "name": "meu-health-check-basico",
  "selfLink": "https://www.googleapis.com/compute/v1/projects/meu-projeto/global/healthChecks/meu-health-check-basico",
  "timeoutSec": 5,
  "type": "HTTP",
  "unhealthyThreshold": 3
}
```

## Opções principais

  * **`http | https | tcp | ssl | http2`**: O tipo de verificação de saúde a ser criada. Você deve especificar um deles no comando (ex: `gcloud compute health-checks create http ...`).
  * `--port`: A porta que será verificada no backend.
  * `--request-path`: (Apenas HTTP/S e HTTP2) O caminho da requisição a ser usado na verificação (ex: `/healthz`).
  * `--check-interval`: O intervalo de tempo entre uma verificação e outra.
  * `--timeout`: O tempo máximo que o GCP aguardará por uma resposta antes de considerar a verificação como falha.
  * `--unhealthy-threshold`: O número de falhas consecutivas para que a VM seja considerada "não saudável".
  * `--healthy-threshold`: O número de sucessos consecutivos para que uma VM "não saudável" volte a ser considerada "saudável".