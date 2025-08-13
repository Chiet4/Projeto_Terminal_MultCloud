# Comando para deletar/apagar uma instância EC2

## Descrição

Comando para finalizar (terminar) uma ou mais instâncias EC2 especificadas. O comando é idempotente: repetir a chamada para uma instância já encerrada não causa erro.
- Após o término, a instância ainda pode ser visualizada por aproximadamente 1 hora.

### Comando para básico para deletar instancias

```bash
aws ec2 terminate-instances --instance-ids <id da instancia>
```

### Comando para testar permissões com `--dry-run`

```bash
aws ec2 terminate-instances \
  --instance-ids ami-07d9b9ddc6cd8dd30 \
  --dry-run
```

## Parâmetros principais

* `--instance-ids`: Um ou mais IDs de instâncias (até 1000 por vez).
* `--dry-run`: Verifica se o usuário tem permissão, sem executar a ação.
* `--cli-input-json` / `--cli-input-yaml`: Fornece entrada estruturada.
* `--generate-cli-skeleton`: Gera estrutura JSON/YAML para entrada ou saída.

## Exemplo de saída

```json
{
  "TerminatingInstances": [
    {
      "InstanceId": "i-1234567890abcdef0",
      "CurrentState": {
        "Code": 32,
        "Name": "shutting-down"
      },
      "PreviousState": {
        "Code": 16,
        "Name": "running"
      }
    }
  ]
}
```

## Códigos de estado da instância

* `0`: pending
* `16`: running
* `32`: shutting-down
* `48`: terminated
* `64`: stopping
* `80`: stopped
