# Comando para registrar targets

## Descrição
Comando para alocar instâncias, IPs, funções Lambda ou ALBs a um Target Group. Os targets registrados passam a receber tráfego do Load Balancer.
- É necessário que a instância EC2 esteja em estado `running`.
- Você pode registrar um mesmo alvo várias vezes com diferentes portas.
- Para tipos `ip`, o alvo pode estar fora da VPC, desde que a zona de disponibilidade seja especificada.
- Para `lambda`, é necessário conceder permissão de invocação ao Load Balancer.

### Comando básico registrar targets

```bash
aws elbv2 register-targets \
  --target-group-arn <arn do seu target group> \
  --targets Id=<id da sua instancia>
```

### 1. Comando para registrar instâncias EC2

```bash
aws elbv2 register-targets \
  --target-group-arn <arn: do Target group> \
  --targets Id=i-xxxxxxxx Id=i-yyyyyyyyy
```

Passa o id das vms criadas e arn do target group.

### 2. Comando para registrar instância com múltiplas portas (ex: containers diferentes na mesma EC2)

```bash
aws elbv2 register-targets \
  --target-group-arn arn:aws:elasticloadbalancing:region:account:targetgroup/meus-targets/abc123 \
  --targets Id=i-0598c7d356eba48d7,Port=80 Id=i-0598c7d356eba48d7,Port=766
```

### 3. Comando para registrar IPs como destino (Target type = `ip`)

```bash
aws elbv2 register-targets \
  --target-group-arn arn:aws:elasticloadbalancing:region:account:targetgroup/ip-targets/xyz987 \
  --targets Id=10.0.1.15 Id=10.0.1.23
```

### 4. Comando para registrar função Lambda

```bash
aws elbv2 register-targets \
  --target-group-arn arn:aws:elasticloadbalancing:region:account:targetgroup/lambda-targets/123abc \
  --targets Id=arn:aws:lambda:region:account:function:minha-funcao
```

## Parâmetros

* `--target-group-arn`: ARN do Target Group.
* `--targets`: Lista de targets a registrar (ID, porta, zona).

  * `Id`: pode ser uma instância, IP, ARN de Lambda, ou outro ALB.
  * `Port`: obrigatório se múltiplos containers/portas.
  * `AvailabilityZone`: pode ser `all` ou uma AZ específica.

## Sintaxe JSON alternativa

```json
[
  {
    "Id": "i-1234567890abcdef0",
    "Port": 80,
    "AvailabilityZone": "us-east-1a"
  }
]
```
