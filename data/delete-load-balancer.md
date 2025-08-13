# Comando excluir load balancer 

## Descrição
Comando que remove um Application Load Balancer (ALB), Network Load Balancer (NLB) ou Gateway Load Balancer (GLB). Também exclui automaticamente os listeners associados.
- A exclusão não remove os targets registrados.
- A instância continua funcionando, mas deixa de receber tráfego do Load Balancer.
- Se o Load Balancer tiver **proteção contra exclusão ativada**, a operação falha.
- Chamar o comando para um LB já excluído não gera erro.

### Comando básico para deletar load balance

```bash
aws elbv2 delete-load-balancer \
  --load-balancer-arn <arn: do load balance>
```

### Requisitos

* Ter permissão `elasticloadbalancing:DeleteLoadBalancer`.
* Desativar a proteção contra exclusão antes, se estiver habilitada.

### Comportamento

* Listeners vinculados ao Load Balancer também são excluídos automaticamente.
* Target Groups **não** são removidos com o Load Balancer.
* Caso deseje remover tudo, exclua os Target Groups separadamente com:

```bash
  aws elbv2 delete-target-group --target-group-arn arn:...
```

## Parâmetros

* `--load-balancer-arn`: ARN do Load Balancer a ser removido.
* `--cli-input-json` / `--cli-input-yaml`: Entrada estruturada alternativa.
* `--generate-cli-skeleton`: Gera estrutura JSON de entrada ou saída.
