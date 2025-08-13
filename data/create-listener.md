# Comando para criar um Listener para um Load Balancer

## Descrição
Comando para cria um listener para um Load Balancer do tipo Application, Network ou Gateway. O listener é responsável por receber conexões na porta especificada e encaminhá-las para o Target Group.
- É obrigatório especificar um **ARN de Load Balancer** e uma **ação padrão**.
- O listener escuta em uma **porta/protocolo** definida e executa ações como:
  - Encaminhar para Target Group
  - Redirecionar
  - Responder com código fixo
  - Autenticar via OIDC ou Cognito

### Comando para criação de um Listener HTTP porta 80 para ALB **Atenção: precisa criar load balance e o target group antes**

```bash
aws elbv2 create-listener \
  --load-balancer-arn <arn: do load balance criando> \
  --protocol HTTP \
  --port 80 \
  --default-actions Type=forward,TargetGroupArn= <arn do target group criado> 
```

### Comando para criar um Listener TCP para NLB

```bash
aws elbv2 create-listener \
  --load-balancer-arn arn:aws:elasticloadbalancing:us-east-1:123456789012:loadbalancer/net/meu-nlb/abc123 \
  --protocol TCP \
  --port 80 \
  --default-actions Type=forward,TargetGroupArn=arn:aws:elasticloadbalancing:us-east-1:123456789012:targetgroup/meu-tg/xyz456
```

## Parâmetros principais

* `--load-balancer-arn`: ARN do Load Balancer
* `--protocol`: `HTTP`, `HTTPS`, `TCP`, `TLS`, `UDP`, `TCP_UDP`, `GENEVE`
* `--port`: Porta de escuta
* `--certificates`: (HTTPS/TLS) ARN de certificado SSL
* `--ssl-policy`: Política de segurança TLS
* `--default-actions`: Ação padrão do listener (ex: `forward`, `redirect`, `fixed-response`)
* `--alpn-policy`: Protocolo ALPN para TLS
* `--tags`: Lista de tags para o listener
* `--mutual-authentication`: Configuração mTLS opcional

---

## Tipos de Ação (`--default-actions`)

* `forward`: Encaminha para um Target Group
* `redirect`: Redireciona requisição HTTP
* `fixed-response`: Retorna uma resposta fixa
* `authenticate-oidc`: Autentica usando OpenID Connect
* `authenticate-cognito`: Autentica via Amazon Cognito

## Exemplo de saída (resumida)

```json
{
  "Listeners": [
    {
      "ListenerArn": "arn:aws:elasticloadbalancing:us-east-1:123456789012:listener/app/meu-alb/abc123/def456",
      "Port": 80,
      "Protocol": "HTTP",
      "DefaultActions": [
        {
          "Type": "forward",
          "TargetGroupArn": "arn:aws:elasticloadbalancing:us-east-1:123456789012:targetgroup/meu-tg/xyz456"
        }
      ]
    }
  ]
}
```
