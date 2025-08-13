# Comando para lista vpcs

## Descrição
Comando para listar informações detalhadas sobre uma ou mais VPCs (Virtual Private Clouds) existentes em sua conta. Pode ser usado para listar todas as VPCs ou consultar uma específica por ID ou filtros.

- Por padrão, retorna todas as VPCs da conta.
- Pode filtrar por CIDR, ID, tags, estado (`pending`, `available`) e mais.
- A operação é paginada. Utilize `--no-paginate` para desativar a paginação automática.

## Exemplos de comando para listar detalhes de vpcs

### 1. Comando para listar todas as VPCs

```bash
aws ec2 describe-vpcs
```

### 2. Comando lista id do VPC default

```bash
aws ec2 describe-vpcs --query 'Vpcs[*].[VpcId]' --output text
```


### 3. Comando para detalhar uma VPC específica

```bash
aws ec2 describe-vpcs \
  --vpc-ids vpc-06e4ab6c6cEXAMPLE
```

### 4. Comando para filtrar VPCs por CIDR

```bash
aws ec2 describe-vpcs \
  --filters Name=cidr,Values=10.0.0.0/16
```

### 5. Comando para filtrar por tag

```bash
aws ec2 describe-vpcs \
  --filters Name=tag:Owner,Values=TimeA
```

## Parâmetros principais

* `--vpc-ids`: Lista de IDs de VPCs (opcional).
* `--filters`: Lista de filtros para limitar os resultados:

  * `cidr`
  * `vpc-id`
  * `state` (`pending`, `available`)
  * `tag`, `tag-key`
  * `is-default`
  * `owner-id`
  * `ipv6-cidr-block-association.state`


## Exemplo de saída resumida

```json
{
  "Vpcs": [
    {
      "VpcId": "vpc-06e4ab6c6cEXAMPLE",
      "CidrBlock": "10.0.0.0/16",
      "State": "available",
      "IsDefault": false,
      "Tags": [
        {
          "Key": "Name",
          "Value": "Shared VPC"
        }
      ]
    }
  ]
}
```

## Paginação

* `--page-size`: Número de resultados por página.
* `--max-items`: Total máximo de itens.
* `--starting-token`: Token para continuar da última consulta.
* `--no-paginate`: Desativa a paginação automática.
