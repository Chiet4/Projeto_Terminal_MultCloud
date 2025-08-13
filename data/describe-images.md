# Comando para listar AMIs 

## Descrição
Comando para lista informações detalhadas sobre imagens (AMIs) disponíveis em sua conta, incluindo públicas, privadas e compartilhadas.
Você pode listar:
- Todas as AMIs acessíveis
- AMIs específicas por ID
- AMIs por proprietário, tags, nome, arquitetura, plataforma, etc.

A resposta inclui detalhes como `ImageId`, `Name`, `State`, `CreationDate`, `RootDeviceType`, `Platform`, `BlockDeviceMappings`, entre outros.

---

### Comando para obter detalhes de uma AMI específica
```bash
aws ec2 describe-images 
```

### Comando para listar AMIs públicas da Amazon

```bash
aws ec2 describe-images \
  --owners amazon \
  --filters Name=is-public,Values=true

```

### Listar AMIs do tipo Windows

```bash
aws ec2 describe-images \
  --owners amazon \
  --filters "Name=platform,Values=windows"
```

### Comando para filtrar por nome da AMI e pega o AMI, retorna em json

```bash
aws ec2 describe-images --owners amazon --filters "Name=name,Values=ubuntu/images/*" \
  --query 'Images[*].{Description: Description, ImageId: ImageId}' --output json
```

### Comando para listar AMIs do Ubuntu com filtro por nome

```bash
aws ec2 describe-images --owners amazon --filters "Name=name,Values=ubuntu/images/*" \
  --query 'Images[*].{Description: Description, ImageId: ImageId}' --output text
```

### Comando para listar AMIs com tag específica

```bash
aws ec2 describe-images \
  --filters "Name=tag:Type,Values=Custom"
```

### Comando para exibir apenas AMI IDs com filtro por tag

```bash
aws ec2 describe-images \
  --filters "Name=tag:Environment,Values=dev" \
  --query "Images[*].ImageId" \
  --output text
```

## Parâmetros úteis

* `--image-ids`: Um ou mais IDs de AMIs.
* `--owners`: Ex: `self`, `amazon`, `aws-marketplace`.
* `--filters`: Lista de filtros como `name`, `platform`, `root-device-type`.
* `--query`: Formata a saída com JMESPath.
* `--output`: `json`, `table`, `text`, `yaml`, etc.
* `--no-paginate`: Útil para evitar paginação automática.
