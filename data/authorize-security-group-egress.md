# Comando para adiciona regras de saída (egress) a um grupo de segurança.

## Descrição
Comando para adiciona regras de **saída (egress)** a um grupo de segurança. Essas regras determinam o tráfego que as instâncias **podem enviar** para fora.
É possível liberar tráfego para:
- Faixas IPv4 ou IPv6
- Prefix lists
- Outros grupos de segurança

A regra exige:
- Um protocolo (`tcp`, `udp`, `icmp`, `icmpv6` ou `-1`)
- Um destino (CIDR, grupo ou prefix list)

### Comando básico liberar trafego de saida do security group

```bash
aws ec2 authorize-security-group-egress \
  --group-id <id do seu sg> \
  --ip-permissions 'IpProtocol=tcp,FromPort=80,ToPort=80,IpRanges=[{CidrIp=10.0.0.0/16}]'
```

### Comando para liberação para outro security group

```bash
aws ec2 authorize-security-group-egress \
  --group-id <id do seu sg> \
  --ip-permissions 'IpProtocol=tcp,FromPort=80,ToPort=80,UserIdGroupPairs=[{GroupId=sg-0aad1c26bbeec5c22}]'
```

## Parâmetros principais

* `--group-id`: ID do grupo de segurança a ser modificado.
* `--ip-permissions`: Lista estruturada com protocolos, portas e destinos.
* `--protocol` / `--port` / `--cidr`: alternativo ao `--ip-permissions` para comandos simples.
* `--tag-specifications`: Tags a serem aplicadas à regra.
* `--dry-run`: Verifica permissões sem executar a alteração.

## Exemplo de comando com descrição e IPv6

```bash
aws ec2 authorize-security-group-egress \
  --group-id <id do seu sg> \
  --ip-permissions 'IpProtocol=tcp,FromPort=443,ToPort=443,Ipv6Ranges=[{CidrIpv6=2001:db8::/64,Description="HTTPS para rede IPv6"}]'
```

## Saída esperada

```json
{
  "Return": true,
  "SecurityGroupRules": [
    {
      "SecurityGroupRuleId": "sgr-0b15794cdb17bf29c",
      "GroupId": "<id do seu sg>",
      "IsEgress": true,
      "IpProtocol": "tcp",
      "FromPort": 80,
      "ToPort": 80,
      "CidrIpv4": "10.0.0.0/16"
    }
  ]
}
```