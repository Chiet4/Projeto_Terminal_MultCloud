# Comando para lista instancia/vms da AWS

## Descrição
O comando para obter informações detalhadas sobre uma ou mais instâncias EC2 em sua conta. Retorna dados sobre todas as instâncias, ou instâncias filtradas por ID, tipo, tags, estado, zona de disponibilidade e outros atributos. A execução sem paginação em ambientes com muitas instâncias pode impactar negativamente a performance.

### Comando para listar todas as instâncias

```bash
aws ec2 describe-instances
```

### Comando para lista id de instancias

```bash
aws ec2 describe-instances \
  --filters "Name=instance-state-name,Values=running" \
  --query "Reservations[*].Instances[*].InstanceId" \
  --output text
```

### Comando para filtrar por tipo de instância

```bash
aws ec2 describe-instances \
  --filters Name=instance-type,Values=t2.micro
```

### Comando para filtrar por tipo de instância e zona de disponibilidade

```bash
aws ec2 describe-instances \
  --filters Name=instance-type,Values=t2.micro \
            Name=availability-zone,Values=us-east-1
```

### Comando para filtrar por tag `Owner`

```bash
aws ec2 describe-instances \
  --filters Name=tag-key,Values=Owner
```

### Comando para filtrar por valor da tag `tag-exemplo`

```bash
aws ec2 describe-instances \
  --filters Name=tag-value,Values=tag-exemplo
```

### Comando para filtrar por tag `Owner=my-team`

```bash
aws ec2 describe-instances \
  --filters Name=tag:Owner,Values=my-team
```

### Comando para exibir apenas os IDs de instância e sub-rede:

```bash
aws ec2 describe-instances \
  --query 'Reservations[*].Instances[*].{Instance:InstanceId,Subnet:SubnetId}' \
  --output json
```

### Comando para exibir apenas os IDs das instâncias `t2.micro`:

```bash
aws ec2 describe-instances \
  --filters Name=instance-type,Values=t2.micro \
  --query "Reservations[*].Instances[*].[InstanceId]" \
  --output text
```

### Comando para exibir ID, AZ e nome (tag `Name`) das instâncias com essa tag:

```bash
aws ec2 describe-instances \
  --filters Name=tag-key,Values=Name \
  --query 'Reservations[*].Instances[*].{Instance:InstanceId,AZ:Placement.AvailabilityZone,Name:Tags[?Key==`Name`]|[0].Value}' \
  --output table
```

## Parâmetros Úteis

* `--instance-ids`: lista de IDs de instâncias.
* `--filters`: permite aplicar diversos critérios (ex: tipo, tags, VPC, estado).
* `--query`: permite filtrar campos específicos na resposta.
* `--output`: formatos de saída como `json`, `table`, `text`.
* `--no-paginate`: desativa paginação automática.

---

## Observações

* Recomendado utilizar paginação (`--page-size`, `--max-items`) para grandes volumes.
* Instâncias recentemente terminadas podem aparecer nos resultados por até 1 hora.
* Instâncias de zonas em falha podem impedir o retorno do comando caso IDs afetados sejam incluídos.
