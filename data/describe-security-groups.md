# Comando para listar Grupo de Segurança (Security Groups)

## Descrição
Comando para listar e obter informações detalhadas sobre grupos de segurança (Security Groups) na sua conta AWS. Pode ser usado com filtros, IDs ou nomes, com suporte a paginação e formatação de saída. Sem argumentos, retorna todos os grupos de segurança. Pode-se filtrar por ID, nome, VPC, regras específicas (porta, IP, protocolo), ou tags. A operação é paginada por padrão.


### Comando básico para listar security groups

```bash
aws ec2 describe-security-groups
```

### Comando para exibir detalhes de um grupo específico

```bash
aws ec2 describe-security-groups \
  --group-ids <id do seu sg>
```

### Comando para testar permissões (Dry Run)

```bash
aws ec2 describe-security-groups \
  --group-ids <id do seu sg> \
  --dry-run
```

### Comando para lista sg com uso de filtros **comando para porta 22 (SSH) e CIDR público:**

```bash
aws ec2 describe-security-groups \
  --filters Name=ip-permission.from-port,Values=22 \
           Name=ip-permission.to-port,Values=22 \
           Name=ip-permission.cidr,Values=0.0.0.0/0 \
  --query "SecurityGroups[*].[GroupName]" \
  --output text
```

### **Comando para listar sg com tags:**

```bash
aws ec2 describe-security-groups \
  --filters Name=group-name,Values=*test* \
           Name=tag:Test,Values=To-delete \
  --query "SecurityGroups[*].{Name:GroupName,ID:GroupId}"
```

## Opções de paginação

* `--max-items`: define o total de grupos a retornar.
* `--page-size`: define o tamanho de cada chamada à API.
* `--starting-token`: continua a partir de uma resposta anterior truncada.
* `--no-paginate`: desativa paginação automática.

## Opções de saída

* `--output`: `json`, `text`, `table`, `yaml`, `yaml-stream`
* `--query`: filtra campos usando [JMESPath](https://jmespath.org/)

## Opções adicionais

* `--group-ids`: lista de IDs (obrigatório para VPC não padrão)
* `--group-names`: nomes (válido apenas em VPC padrão)
* `--filters`: lista de filtros por atributos ou tags
* `--cli-input-json` | `--cli-input-yaml`: entrada estruturada
* `--generate-cli-skeleton`: gera modelos JSON/YAML para entrada ou saída
