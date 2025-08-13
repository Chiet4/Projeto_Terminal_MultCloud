# Comando para criar um Load Balancer

## Descrição
Comando para cria um Load Balancer no Amazon ELB v2. Pode ser dos tipos: Application Load Balancer (ALB), Network Load Balancer (NLB) ou Gateway Load Balancer (GLB).
- Load Balancers direcionam tráfego para instâncias registradas em Target Groups.
- O tipo (`application`, `network` ou `gateway`) determina o comportamento, camadas e recursos.
- É necessário especificar pelo menos duas subnets para balanceadores públicos em múltiplas zonas.

### Comando para criação de um load balance 
```bash
aws elbv2 create-load-balancer \
  --name meu-alb \
  --subnets subnet-a1 subnet-b2 \
  --security-groups sg-12345678 \
  --scheme internet-facing \
  --type application
```

IMPORTANTE - Precisa especificar duas subnets. 

### Comando para criar um Load Balancer público

```bash
aws elbv2 create-load-balancer \
  --name meu-alb \
  --subnets subnet-a1 subnet-b2 \
  --security-groups sg-abcd1234 \
  --scheme internet-facing \
  --type application
```

### Comando para criar um Load Balancer interno

```bash
aws elbv2 create-load-balancer \
  --name meu-alb-interno \
  --subnets subnet-a1 subnet-b2 \
  --security-groups sg-abcd1234 \
  --scheme internal \
  --type application
```

### Comando para criar um Network Load Balancer com o EIP fixo

```bash
aws elbv2 create-load-balancer \
  --name meu-nlb \
  --type network \
  --subnet-mappings SubnetId=subnet-a1,AllocationId=eipalloc-abc123
```

### Comando para criar um Gateway Load Balancer

```bash
aws elbv2 create-load-balancer \
  --name meu-glb \
  --type gateway \
  --subnets subnet-a1 subnet-b2
```

### Comando para lista o DNS:

```bash
aws elbv2 describe-load-balancers \
  --names <nome do alb> \
  --query "LoadBalancers[0].DNSName" --output text
```

## Principais parâmetros

* `--name`: Nome único do Load Balancer (até 32 caracteres).
* `--subnets`: IDs das subnets (mínimo 2 para ALB público).
* `--subnet-mappings`: Mapeamento com IPs fixos, se necessário.
* `--security-groups`: IDs de grupos de segurança (obrigatório para ALB).
* `--scheme`: Tipo de acesso (`internet-facing` ou `internal`).
* `--type`: Tipo do Load Balancer (`application`, `network`, `gateway`).
* `--ip-address-type`: IPv4 padrão ou `dualstack` (IPv4 + IPv6).
* `--tags`: Lista de tags associadas (`Key=...,Value=...`).

## Exemplo de saída (resumido)

```json
{
  "LoadBalancers": [
    {
      "LoadBalancerArn": "arn:aws:elasticloadbalancing:...",
      "DNSName": "meu-alb-123456.elb.us-east-1.amazonaws.com",
      "Scheme": "internet-facing",
      "VpcId": "vpc-abc123",
      "State": { "Code": "provisioning" },
      "Type": "application"
    }
  ]
}
```