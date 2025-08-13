# Comando para lista Sub redes - Subnets

## Descrição
Comando para listar informações sobre sub-nets em sua conta. Por padrão, lista todas as subnets existentes. É possível filtrar por VPC, tags, estado, zona de disponibilidade, entre outros.
- Comando paginado: usa `--max-items`, `--page-size`, `--starting-token`.
- Pode ser usado com filtros por ID, VPC, CIDR, AZ, entre outros.
- Pode retornar metadados como IPv6, DNS, e informações de tags.

## Exemplos de comandos para lista subnets

### 1. Comando para listar todas as subnets

```bash
aws ec2 describe-subnets
```

### 2. Comando para identificar as subnets 

```bash
aws ec2 describe-subnets \
  --filters "Name=vpc-id,Values=vpc-xxxxxxxxxxxxxxxxx" \
  --query 'Subnets[*].[SubnetId,AvailabilityZone]' \
  --output table
```

### 3. Comando para listar subnets com tag específica

```bash
aws ec2 describe-subnets \
  --filters "Name=tag:CostCenter,Values=123" \
  --query "Subnets[*].SubnetId" \
  --output text
```

---

## Exemplo de saída (resumido)

```json
{
  "Subnets": [
    {
      "SubnetId": "subnet-0bb1c79de3EXAMPLE",
      "VpcId": "vpc-0ee975135dEXAMPLE",
      "CidrBlock": "172.31.80.0/20",
      "AvailabilityZone": "us-east-1d",
      "MapPublicIpOnLaunch": false,
      "State": "available",
      "DefaultForAz": true,
      "Tags": [
        { "Key": "Name", "Value": "MySubnet" }
      ]
    }
  ]
}
```

## Filtros suportados

* `vpc-id`
* `subnet-id`
* `availability-zone` ou `availability-zone-id`
* `cidr-block` ou `ipv6-cidr-block-association.ipv6-cidr-block`
* `state`: `available`, `pending`
* `tag:<key>` ou `tag-key`
* `map-public-ip-on-launch`
* `ipv6-native`
* `default-for-az`
* `owner-id`
* `enable-dns64`

## Parâmetros úteis

* `--subnet-ids`: Lista de IDs de subnet.
* `--filters`: Filtros detalhados para busca.
* `--query`: Filtra saída com JMESPath.
* `--output`: `json`, `table`, `text`, etc.
* `--no-paginate`: Evita paginação automática.
* `--starting-token`: Continua paginação anterior.
