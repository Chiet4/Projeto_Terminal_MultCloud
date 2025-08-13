# Comando para adicionar regras de entrada (ingress) a um grupo de segurança

## Descrição
Comando para adiciona regras de entrada (ingress) a um grupo de segurança, permitindo que instâncias recebam tráfego de fontes específicas. Pode ser usado com CIDRs IPv4/IPv6, prefix lists ou outros grupos de segurança.
Cada regra deve especificar um protocolo (`tcp`, `udp`, `icmp`, `icmpv6`, ou `-1` para todos), e quando aplicável, portas ou faixas de portas.

A propagação para instâncias é quase imediata, mas pode ocorrer um pequeno atraso.

### Comando básico para liberar trafego de entrada no security group 

```bash
aws ec2 authorize-security-group-ingress \
  --group-id <id do seu sg> \
  --protocol tcp \
  --port 22 \
  --cidr 203.0.113.0/24
```
## Exemplos de comandos 

### 1. Comando para acesso via outro grupo de segurança (mesma VPC)

```bash
aws ec2 authorize-security-group-ingress \
  --group-id <id do seu sg> \
  --protocol tcp \
  --port 80 \
  --source-group sg-1a2b3c4d
```

### 2. Comando para liberr porta 80 e 22 

```bash
aws ec2 authorize-security-group-ingress \
  --group-name flask-sg \
  --protocol tcp --port 80 --cidr 0.0.0.0/0
```
```bash
aws ec2 authorize-security-group-ingress \
  --group-name flask-sg \
  --protocol tcp --port 22 --cidr 0.0.0.0/0
```

### 3. Comando para múltiplas regras (RDP e ICMP)

```bash
aws ec2 authorize-security-group-ingress \
  --group-id <id do seu sg> \
  --ip-permissions 'IpProtocol=tcp,FromPort=3389,ToPort=3389,IpRanges=[{CidrIp=172.31.0.0/16}]' \
                   'IpProtocol=icmp,FromPort=-1,ToPort=-1,IpRanges=[{CidrIp=172.31.0.0/16}]'
```

### 4. Comando para ICMP específico (type 3, code 4)

```bash
aws ec2 authorize-security-group-ingress \
  --group-id <id do seu sg> \
  --ip-permissions 'IpProtocol=icmp,FromPort=3,ToPort=4,IpRanges=[{CidrIp=0.0.0.0/0}]'
```

### 5. Comando para IPv6 para SSH

```bash
aws ec2 authorize-security-group-ingress \
  --group-id <id do seu sg> \
  --ip-permissions 'IpProtocol=tcp,FromPort=22,ToPort=22,Ipv6Ranges=[{CidrIpv6=2001:db8:1234:1a00::/64}]'
```

### 6. Comando para ICMPv6 de qualquer origem

```bash
aws ec2 authorize-security-group-ingress \
  --group-id <id do seu sg> \
  --ip-permissions 'IpProtocol=icmpv6,Ipv6Ranges=[{CidrIpv6=::/0}]'
```

### 7. Comando com regra e descrição

```bash
aws ec2 authorize-security-group-ingress \
  --group-id <id do seu sg> \
  --ip-permissions 'IpProtocol=tcp,FromPort=3389,ToPort=3389,IpRanges=[{CidrIp=203.0.113.0/24,Description="RDP access from NY office"}]'
```

### 8. Comando com regra e prefix list

```bash
aws ec2 authorize-security-group-ingress \
  --group-id <id do seu sg> \
  --ip-permissions 'IpProtocol=-1,PrefixListIds=[{PrefixListId=pl-002dc3ec097de1514}]'
```

## Parâmetros úteis

* `--group-id`: ID do grupo de segurança
* `--protocol`: `tcp`, `udp`, `icmp`, `icmpv6`, ou `-1` para todos
* `--port`: Porta ou faixa (ex: `80`, `1024-2048`)
* `--cidr`: Faixa CIDR IPv4
* `--source-group`: Grupo de origem
* `--ip-permissions`: JSON estruturado com múltiplas regras
* `--tag-specifications`: Tags associadas
* `--dry-run`: Verifica permissões sem executar