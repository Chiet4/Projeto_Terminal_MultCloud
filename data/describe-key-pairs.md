# Comando para listar pares de chaves 

## Descrição
Comando para recuperar informações sobre os pares de chaves EC2 existentes na conta da AWS. Pode retornar dados como nome, tipo, fingerprint, data de criação, tags e material da chave pública.

- Retorna todos os pares de chave, ou apenas os especificados.
- É possível buscar por nome (`--key-names`), ID (`--key-pair-ids`), ou aplicar filtros.
- É possível incluir o conteúdo da chave pública com `--include-public-key`.

### 1. Comando para listar todos os pares de chaves

```bash
aws ec2 describe-key-pairs
```

### 2. Comando para listar uma chave específica por nome

```bash
aws ec2 describe-key-pairs --key-names minha-chave
```

### 3. Comando para lista chave com material da chave pública

```bash
aws ec2 describe-key-pairs \
  --key-names minha-chave \
  --include-public-key
```

### 4. Comando para buscar por tag

```bash
aws ec2 describe-key-pairs \
  --filters Name=tag:Owner,Values=TimeDev
```

## Exemplo de saída

```json
{
  "KeyPairs": [
    {
      "KeyPairId": "key-0b94643da6EXAMPLE",
      "KeyFingerprint": "1f:51:ae:28:...:f5:f1:6f",
      "KeyName": "minha-chave",
      "KeyType": "rsa",
      "Tags": [],
      "CreateTime": "2022-05-27T21:51:16.000Z"
    }
  ]
}
```

## Parâmetros principais

* `--key-names`: Lista de nomes de chave a consultar.
* `--key-pair-ids`: Lista de IDs de chave.
* `--filters`: Filtros como:

  * `key-name`
  * `key-pair-id`
  * `fingerprint`
  * `tag:<chave>`
* `--include-public-key`: Inclui o material da chave pública na resposta.
* `--dry-run`: Verifica permissões sem executar a chamada.
