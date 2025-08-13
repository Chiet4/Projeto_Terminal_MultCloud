# Comando para criaçao de grupo de segurança (security group)

## Descrição
Comando para cria um grupo de segurança (security group), que atua como firewall virtual para controlar tráfego de entrada e saída de instâncias EC2. É possível associar o grupo a uma VPC específica e adicionar tags durante a criação. Um grupo de segurança define regras de tráfego (inbound e outbound). Ao criar, é necessário fornecer um nome único (por VPC) e uma descrição. A AWS oferece um grupo padrão, mas este comando permite criar novos com regras personalizadas.

### Comando para criar um security group 

```bash
aws ec2 create-security-group \
  --group-name <MeuGrupoDeSeguranca> \
  --description "Grupo para acesso HTTP e SSH" \
```

Você pode adicionar tags no momento da criação usando a flag `--tag-specifications`.

### Comando para criar um security group com tags (Opcional):

```bash
aws ec2 create-security-group \
  --group-name MeuGrupoDeSeguranca \
  --description "Grupo para EC2" \
  --tag-specifications 'ResourceType=security-group,Tags=[{Key=Ambiente,Value=Producao}]'
```

### Teste de permissão com `--dry-run`

```bash
aws ec2 create-security-group \
  --group-name MeuGrupoTeste \
  --description "Teste de permissão" \
  --vpc-id <id do seu vpc> \
  --dry-run
```
Retorno esperado:

* Se permitido: `DryRunOperation`
* Se não permitido: `UnauthorizedOperation`




## Saída esperada

```json
{
  "GroupId": "sg-903004f8"
}
```
## Opções principais

* `--group-name`: Nome amigável do grupo (até 255 caracteres, não pode começar com `sg-`)
* `--description`: Descrição do grupo (até 255 caracteres)
* `--vpc-id`: ID da VPC onde o grupo será criado (obrigatório em VPCs não-default)
* `--tag-specifications`: Lista de tags a serem associadas