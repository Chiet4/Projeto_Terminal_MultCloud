# Comando para criar uma Regra de Encaminhamento (Forwarding Rule)

## Descrição

Este comando cria uma Regra de Encaminhamento, que é a "porta de entrada" (frontend) de um Load Balancer do Google Cloud. A regra vincula um endereço IP e uma porta específicos a um recurso de destino (como um Target Proxy). É o passo final que expõe toda a sua configuração de balanceamento de carga para a internet ou para sua rede VPC.

Sem uma regra de encaminhamento, seu Load Balancer está configurado, mas não pode receber tráfego.

### Comando para criar uma Regra de Encaminhamento para um LB HTTP

Este exemplo conclui a configuração do Load Balancer que montamos nos passos anteriores, direcionando o tráfego da porta 80 para nosso proxy HTTP.

```bash
gcloud compute forwarding-rules create http-frontend-rule \
    --address <ip-load-balancer-global> \
    --target-http-proxy <meu-proxy-http> \
    --ports=80 \
    --global \
    --description="Regra de entrada para o LB de frontend"
```

### Contexto: O Quebra-Cabeça Completo

Este comando é o passo final. A sequência completa para criar um Load Balancer HTTP do zero é:

1.  `health-checks create`: Para verificar a saúde das VMs.
2.  `backend-services create`: Para agrupar os backends.
3.  `url-maps create`: Para definir as regras de roteamento baseadas em URL.
4.  `target-http-proxies create`: Para receber o tráfego e usar o mapa de URLs.
5.  `addresses create`: Para reservar um IP estático.
6.  **`forwarding-rules create`**: Para vincular o IP e a porta ao proxy e ativar o Load Balancer.

## Saída esperada

```json
{
  "IPAddress": "34.68.123.45",
  "IPProtocol": "TCP",
  "creationTimestamp": "2025-07-04T09:48:30.123-03:00",
  "description": "Regra de entrada para o LB de frontend",
  "id": "1234567890123456789",
  "kind": "compute#forwardingRule",
  "loadBalancingScheme": "EXTERNAL",
  "name": "http-frontend-rule",
  "networkTier": "PREMIUM",
  "portRange": "80-80",
  "selfLink": "https://www.googleapis.com/compute/v1/projects/meu-projeto/global/forwardingRules/http-frontend-rule",
  "target": "https://www.googleapis.com/compute/v1/projects/meu-projeto/global/targetHttpProxies/meu-proxy-http"
}
```

## Opções principais

  * `--address`: **(Obrigatório)** O nome do endereço IP estático (criado com `addresses create`) que será usado por esta regra.
  * `--target-http-proxy`, `--target-https-proxy`, `--target-pool`, etc.: **(Obrigatório)** O recurso de destino para o qual o tráfego será encaminhado. O tipo de destino deve ser compatível com o tipo de Load Balancer.
  * `--ports`: **(Obrigatório)** A porta, lista de portas ou intervalo de portas que esta regra irá escutar. Ex: `80`, `80,8080`, `80-90`.
  * `--global` ou `--region`: Define o escopo da regra. Deve ser consistente com o escopo do endereço IP e do recurso de destino.
  * `--load-balancing-scheme`: O tipo de balanceamento de carga. Ex: `EXTERNAL`, `INTERNAL_MANAGED`.