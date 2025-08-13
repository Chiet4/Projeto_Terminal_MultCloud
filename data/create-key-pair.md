# Comando para criar par de chaves (key pair)

## Descrição
Comando para cria um novo par de chaves (key pair) EC2 do tipo `rsa` ou `ed25519`. A chave pública é armazenada pela AWS, e a chave privada é retornada como PEM ou PPK (formato PuTTY).
- A chave privada é exibida uma única vez no momento da criação.
- Você pode ter até **5.000 key pairs por região**.
- Use `rsa` para Windows (ED25519 não é suportado).
- A chave criada é válida apenas na região atual.
- Para reutilizar em outra região, use `import-key-pair`.

### Comando simples para criar um par de chaves (formato padrão PEM)

```bash
  aws ec2 create-key-pair \
    --key-name minha-chave \
    --query 'KeyMaterial' \
    --output text > minha-chave.pem
```

**Resultado esperado:**

Não retorna nada, porém a chave estará criada na nuvem e na pasta local que executaste o comando. Rode um `ls` na pasta para ver.

### Exemplo: chave no formato PPK (para uso com PuTTY)

```bash
aws ec2 create-key-pair \
  --key-name MyKeyPair \
  --key-format ppk
```

### Exemplo com tags

```bash
aws ec2 create-key-pair \
  --key-name MyKeyPair \
  --tag-specifications 'ResourceType=key-pair,Tags=[{Key=Project,Value=MonitoriaDevOps}]'
```

## Parâmetros principais

* `--key-name`: Nome único da chave (obrigatório).
* `--key-type`: `rsa` (padrão) ou `ed25519`.
* `--key-format`: `pem` (padrão) ou `ppk`.
* `--tag-specifications`: Lista de tags no formato:
* `--dry-run`: Verifica permissões sem criar a chave.

## Cuidados

* **Salve a chave privada imediatamente.** A AWS **não armazena** a chave após exibição.
* Se tentar recriar uma chave com o mesmo nome, o comando falha.
* Para importar chaves criadas externamente, use `import-key-pair`.