# Comando para apagar grupo de segurança (security group)

## Descrição
Comando para apagar um grupo de segurança (security group) da sua conta na AWS. O grupo não pode estar associado a nenhuma instância, interface de rede ou ser referenciado por outro grupo de segurança dentro da mesma VPC. Se o grupo estiver associado a algum recurso, a operação falhará com o erro `DependencyViolation`.

### Comando para deletar sg por ID (obrigatório em VPCs não-default):

```bash
aws ec2 delete-security-group --group-id <id do seu sg>
```

### Comando para deletar sg por nome (somente em VPC default):

```bash
aws ec2 delete-security-group --group-name MySecurityGroup
```

## Teste com `--dry-run`

```bash
aws ec2 delete-security-group \
  --group-id <id do seu sg> \
  --dry-run
```

Se tiver permissão, a resposta será `DryRunOperation`. Caso contrário, será `UnauthorizedOperation`.

## Parâmetros disponíveis

* `--group-id`: ID do grupo de segurança (necessário para VPCs não default)
* `--group-name`: Nome do grupo (válido apenas em VPC default)
* `--dry-run`: Simula a operação para verificar permissões
* `--cli-input-json` / `--cli-input-yaml`: Entrada estruturada via JSON/YAML
* `--generate-cli-skeleton`: Gera esqueleto para entrada/saída

## Saída esperada

Se bem-sucedido, nenhum output será retornado.

---

## Restrições

* Não é possível excluir um grupo enquanto ele estiver associado a instâncias, interfaces de rede ou referenciado por outro grupo na mesma VPC.
* Em VPCs não-default, é necessário usar o ID do grupo, não o nome.