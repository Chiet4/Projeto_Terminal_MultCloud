# Comando para criar (reservar) um Endereço IP Estático (Address)

## Descrição

Este comando reserva um endereço IP estático, que pode ser regional ou global, interno ou externo. Endereços IP estáticos são essenciais para garantir um ponto de acesso fixo para suas aplicações, permitindo que você configure registros de DNS permanentes e forneça acesso confiável a recursos como VMs e Load Balancers.

Ao reservar um endereço, ele pertence à sua conta até que você decida liberá-lo.

### Comando para reservar um IP Externo Global

Ideal para ser usado com um Load Balancer de Aplicativo Externo Global.

```bash
gcloud compute addresses create ip-load-balancer-global \
    --ip-version=IPV4 \
    --global \
    --description="IP global para o LB de frontend"
```

### Comando para reservar um IP Externo Regional

Perfeito para ser associado a uma única máquina virtual (VM).

```bash
gcloud compute addresses create ip-vm-servidor-web \
    --region=us-central1
```

## Saída esperada (do comando regional)

```json
{
  "address": "34.68.123.45",
  "addressType": "EXTERNAL",
  "creationTimestamp": "2025-07-04T09:38:00.123-03:00",
  "description": "",
  "id": "1234567890123456789",
  "ipVersion": "IPV4",
  "kind": "compute#address",
  "name": "ip-vm-servidor-web",
  "networkTier": "PREMIUM",
  "region": "https://www.googleapis.com/compute/v1/projects/meu-projeto/regions/us-central1",
  "selfLink": "https://www.googleapis.com/compute/v1/projects/meu-projeto/regions/us-central1/addresses/ip-vm-servidor-web",
  "status": "RESERVED"
}
```

## Opções principais

  * `--description`: Uma descrição textual para o endereço IP.
  * `--region`: Para endereços regionais. Usado para recursos dentro de uma região específica, como uma VM.
  * `--global`: Para endereços globais. Usado para recursos globais, como Load Balancers de Aplicativo Externos.
  * `--address-type`: Especifica se o endereço é `EXTERNAL` (público, padrão) ou `INTERNAL` (privado, dentro da sua VPC).
  * `--ip-version`: A versão do IP, `IPV4` ou `IPV6`. O padrão é `IPV4`.
  * `--subnet`: (Obrigatório para IPs internos) A sub-rede da VPC da qual o endereço interno será alocado.