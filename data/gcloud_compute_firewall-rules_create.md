# Comando para criar uma regra de firewall (firewall rule)

## Descrição

Comando para criar uma regra de firewall no GCP. As regras de firewall controlam o tráfego de entrada (ingress) e saída (egress) para instâncias de VM dentro de uma rede VPC. As regras são aplicadas a instâncias que possuem *tags* de rede específicas, permitindo um controle granular e escalável do acesso. Por padrão, todo tráfego de entrada é bloqueado, enquanto todo tráfego de saída é permitido.

### Comando para criar uma regra de firewall (Ex: permitir SSH)

```bash
gcloud compute firewall-rules create permitir-ssh \
    --network minha-rede \
    --allow tcp:22 \
    --source-ranges 0.0.0.0/0 \
    --description "Permite conexões SSH de qualquer IP" \
    --target-tags ssh-permitido
```

Este comando cria uma regra chamada `permitir-ssh` que libera a porta 22 (TCP) para qualquer endereço de origem (`0.0.0.0/0`) em instâncias na rede `minha-rede` que tenham a tag `ssh-permitido`.

### Comando para criar uma regra de firewall para tráfego HTTP

```bash
gcloud compute firewall-rules create permitir-http \
    --network default \
    --allow tcp:80 \
    --source-ranges 0.0.0.0/0 \
    --description "Permite tráfego HTTP para servidores web" \
    --target-tags http-server
```

Este comando cria uma regra na rede `default` para permitir tráfego na porta 80 (HTTP) para todas as VMs com a tag `http-server`.

### Comando Essencial: Permitir Verificações de Saúde (Health Check) do Load Balancer

```bash
gcloud compute firewall-rules create permitir-health-check \
    --network default \
    --action allow \
    --direction INGRESS \
    --source-ranges 35.191.0.0/16,130.211.0.0/22,209.85.152.0/22,209.85.204.0/22 \
    --target-tags http-server \
    --rules tcp:80
```

Este comando cria uma regra que permite que apenas os sistemas de verificação de saúde do GCP acessem a porta 80 das VMs com a tag http-server. Sem esta regra, suas instâncias podem ser incorretamente marcadas como UNHEALTHY, fazendo com que o Load Balancer não envie tráfego para elas.

## Saída esperada

```json
{
  "allowed": [
    {
      "IPProtocol": "tcp",
      "ports": [
        "22"
      ]
    }
  ],
  "creationTimestamp": "2023-10-27T12:00:00.123-07:00",
  "description": "Permite conexões SSH de qualquer IP",
  "direction": "INGRESS",
  "id": "1234567890123456789",
  "kind": "compute#firewall",
  "name": "permitir-ssh",
  "network": "https://www.googleapis.com/compute/v1/projects/meu-projeto/global/networks/minha-rede",
  "priority": 1000,
  "selfLink": "https://www.googleapis.com/compute/v1/projects/meu-projeto/global/firewalls/permitir-ssh",
  "sourceRanges": [
    "0.0.0.0/0"
  ],
  "targetTags": [
    "ssh-permitido"
  ]
}
```

## Opções principais

  * `--allow`: A lista de protocolos e portas a serem permitidos. Ex: `tcp:80`, `udp:5000-5010`, `icmp`.
  * `--description`: Uma descrição textual para a regra de firewall.
  * `--network`: A rede VPC na qual a regra será criada. O padrão é `default`.
  * `--source-ranges`: Blocos de IP de origem (em formato CIDR) aos quais a regra se aplica. O padrão é `0.0.0.0/0` (qualquer origem).
  * `--target-tags`: Uma lista de *tags* de rede. A regra será aplicada a todas as instâncias que possuírem uma dessas tags.
  * `--direction`: A direção do tráfego (`INGRESS` para entrada ou `EGRESS` para saída). O padrão é `INGRESS`.
  * `--action`: A ação a ser tomada quando a condição é correspondida (`ALLOW` ou `DENY`). O padrão é `ALLOW`.