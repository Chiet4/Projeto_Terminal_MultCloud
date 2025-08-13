# Comando para listar informações detalhadas sobre um ou mais Load Balancers

## Descrição
Comando para listar informações detalhadas sobre um ou mais Load Balancers. Pode ser usado para listar todos os ALBs, NLBs e GLBs da conta.
Esse comando suporta:
- Busca por nome (`--names`)
- Busca por ARN (`--load-balancer-arns`)
- Paginação de grandes volumes de dados com `--max-items` e `--starting-token`
- Filtros e extração de dados específicos com `--query`

## Exemplo básico de comandos para descrever load balances

### Comando para listar todos os Load Balancers
```bash
aws elbv2 describe-load-balancers
```

### Comando para buscar por nome

```bash
aws elbv2 describe-load-balancers --names meu-alb
```

### Comando para buscar por ARN

```bash
aws elbv2 describe-load-balancers \
  --load-balancer-arns <arn: do load balance>
```

## Exemplo de saída

```json
{
  "LoadBalancers": [
    {
      "LoadBalancerArn": "arn:aws:elasticloadbalancing:us-west-2:123456789012:loadbalancer/app/my-load-balancer/50dc6c495c0c9188",
      "DNSName": "my-load-balancer-424835706.us-west-2.elb.amazonaws.com",
      "VpcId": "vpc-3ac0fb5f",
      "State": {
        "Code": "active"
      },
      "Type": "application",
      "Scheme": "internet-facing",
      "AvailabilityZones": [
        {
          "ZoneName": "us-west-2a",
          "SubnetId": "subnet-8360a9e7"
        },
        {
          "ZoneName": "us-west-2b",
          "SubnetId": "subnet-b7d581c0"
        }
      ],
      "SecurityGroups": ["sg-5943793c"],
      "IpAddressType": "ipv4"
    }
  ]
}
```

## Parâmetros úteis

* `--load-balancer-arns`: Um ou mais ARNs de Load Balancer (até 20).
* `--names`: Lista de nomes de Load Balancers.
* `--page-size`: Número de itens por chamada da API (não afeta a saída final).
* `--max-items`: Número total de itens retornados pela CLI.
* `--starting-token`: Token para continuar paginação anterior.
* `--no-paginate`: Desativa paginação automática.
* `--query`: Expressão JMESPath para filtrar a saída.
* `--output`: Formato da saída (json, table, text, etc).

## Estados possíveis do Load Balancer

* `provisioning`: sendo criado
* `active`: pronto para uso
* `active_impaired`: ativo, mas com restrições
* `failed`: falha ao criar
