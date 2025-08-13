# Comando para lista Target Groups

## Descrição
Comando para listar todos os Target Groups existentes na conta ou recupera detalhes de Target Groups específicos com base em nome, ARN ou Load Balancer associado.

- A operação é paginada por padrão.
- Suporta busca por:
  - Nome do target group (`--names`)
  - ARN do target group (`--target-group-arns`)
  - ARN do Load Balancer (`--load-balancer-arn`)
- Também permite paginação manual com `--page-size`, `--max-items`, `--starting-token`.

### Exemplo de comando básico para listar target groups

```bash
aws elbv2 describe-target-groups
```

### Comando para buscar Target Group por ARN

```bash
aws elbv2 describe-target-groups \
  --target-group-arns <arn: do seu target group>
```

### Comando para buscar Target Groups de um Load Balancer

```bash
aws elbv2 describe-target-groups \
  --load-balancer-arn <arn: da sua load balance> \
  --query TargetGroups[*].TargetGroupName
```

## Exemplo de saída resumida

```json
{
  "TargetGroups": [
    {
      "TargetGroupArn": "arn:aws:elasticloadbalancing:us-west-2:123456789012:targetgroup/my-targets/73e2d6bc24d8a067",
      "TargetGroupName": "my-targets",
      "Protocol": "HTTP",
      "Port": 80,
      "VpcId": "vpc-3ac0fb5f",
      "HealthCheckProtocol": "HTTP",
      "HealthCheckPort": "traffic-port",
      "HealthCheckEnabled": true,
      "HealthCheckIntervalSeconds": 30,
      "HealthCheckTimeoutSeconds": 5,
      "HealthyThresholdCount": 5,
      "UnhealthyThresholdCount": 2,
      "HealthCheckPath": "/",
      "Matcher": {
        "HttpCode": "200"
      },
      "LoadBalancerArns": [
        "arn:aws:elasticloadbalancing:us-west-2:123456789012:loadbalancer/app/my-load-balancer/50dc6c495c0c9188"
      ],
      "TargetType": "instance",
      "ProtocolVersion": "HTTP1",
      "IpAddressType": "ipv4"
    }
  ]
}
```

## Parâmetros

* `--load-balancer-arn`: Lista todos os Target Groups de um ALB/NLB específico.
* `--target-group-arns`: Lista um ou mais Target Groups por ARN.
* `--names`: Lista Target Groups por nome.
* `--max-items`: Limita o total de itens retornados.
* `--page-size`: Controla o tamanho de cada chamada.
* `--starting-token`: Continua uma listagem paginada anterior.
* `--no-paginate`: Desativa paginação automática.
* `--query`: Expressão JMESPath para extrair dados.
* `--output`: Define o formato da saída (ex: `json`, `table`, `text`).
