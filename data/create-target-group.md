# Comando para criar Target Group

## Descrição
Comando para cria um Target Group no Amazon Elastic Load Balancing (v2). É necessário para que um Load Balancer direcione tráfego para instâncias EC2, IPs, funções Lambda ou outros ALBs.
- Suporta protocolos: `HTTP`, `HTTPS`, `TCP`, `TLS`, `UDP`, `TCP_UDP`, `GENEVE`.
- O Target Group define:
  - Protocolo e porta dos destinos
  - Tipo dos alvos (instância, IP, Lambda, ALB)
  - Parâmetros de health check
- Cada Target Group pode estar associado a apenas um Load Balancer.

### Comando para criar um target group EC2 padrão tipo `instance`

```bash
aws elbv2 create-target-group \
  --name meus-targets \
  --protocol HTTP \
  --port 80 \
  --target-type instance \
  --vpc-id vpc-0a1b2c3d4e5f6g7h8
```

### Comando para criar target group para função Lambda

```bash
aws elbv2 create-target-group \
  --name lambda-target \
  --target-type lambda
```

### Comando para criar target group com IPs (usado com NLB)

```bash
aws elbv2 create-target-group \
  --name ip-targets \
  --protocol TCP \
  --port 80 \
  --target-type ip \
  --vpc-id vpc-0a1b2c3d4e5f6g7h8
```

### Comando para criar Target Group com outro ALB como alvo (target-type alb)

```bash
aws elbv2 create-target-group \
  --name alb-target \
  --protocol TCP \
  --port 80 \
  --target-type alb \
  --vpc-id vpc-0a1b2c3d4e5f6g7h8
```

## Parâmetros importantes

* `--name`: Nome único (até 32 caracteres)
* `--protocol`: Protocolo de roteamento
* `--port`: Porta do destino (ex: 80)
* `--target-type`: Tipo de destino (`instance`, `ip`, `lambda`, `alb`)
* `--vpc-id`: VPC usada (exceto para Lambda)
* `--ip-address-type`: IPv4 ou IPv6
* `--health-check-*`: Parâmetros de verificação de saúde
* `--matcher`: Código HTTP ou gRPC considerado como resposta válida
* `--tags`: Lista de tags (chave=valor)

---

## Parâmetros de health check padrão

* `--health-check-protocol`: `HTTP` (ALB), `TCP` (NLB)
* `--health-check-path`: Caminho de verificação (`/`)
* `--health-check-interval-seconds`: 30
* `--health-check-timeout-seconds`: 5 (HTTP), 10 (TCP)
* `--healthy-threshold-count`: 5
* `--unhealthy-threshold-count`: 2

## Exemplo de saída resumida

```json
{
  "TargetGroups": [
    {
      "TargetGroupArn": "arn:aws:elasticloadbalancing:...:targetgroup/meus-targets/abc123",
      "TargetGroupName": "meus-targets",
      "Protocol": "HTTP",
      "Port": 80,
      "VpcId": "vpc-0a1b2c3d",
      "TargetType": "instance",
      "HealthCheckEnabled": true
    }
  ]
}
```