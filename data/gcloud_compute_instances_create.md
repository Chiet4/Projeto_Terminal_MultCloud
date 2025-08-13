# Comando para criar uma ou mais instâncias de VM no GCP.

## Descrição

Esse comando é a forma principal de criar uma nova máquina virtual (VM) no Google Cloud Platform (GCP). Sem fornecer configurações de disco, o GCP provisiona automaticamente um disco de inicialização persistente com base na imagem usada. A ferramenta de linha de comando `gcloud` é uma alternativa ao uso da API do Compute Engine e permite gerenciar todos os recursos.

### Exemplo básico de comando para criar uma VM

```bash
gcloud compute instances create minha-vm \
    --image-family ubuntu-2204-lts \
    --image-project ubuntu-os-cloud \
    --machine-type e2-micro \
    --zone us-central1-a
```

Este comando:

  - Cria 1 instância de VM com o nome `minha-vm`.
  - Utiliza a família de imagens `ubuntu-2204-lts` (Ubuntu 22.04 LTS) do projeto `ubuntu-os-cloud`.
  - Usa o tipo de máquina `e2-micro`.
  - Implanta a VM na zona `us-central1-a`.

O Google Cloud associa automaticamente um disco de inicialização à VM.

### Exemplo de comando passando uma sub-rede específica

```bash
gcloud compute instances create minha-vm-rede \
    --image-family ubuntu-2204-lts \
    --image-project ubuntu-os-cloud \
    --machine-type e2-micro \
    --zone us-central1-a \
    --subnet minha-sub-rede \
    --tags http-server,https-server
```

Este exemplo adiciona a flag `--subnet` para especificar uma sub-rede e a flag `--tags`, que pode ser usada para aplicar regras de firewall.

### Exemplo de comando com script de inicialização (Startup Script)

O GCP usa metadados para passar scripts de inicialização. O script é executado sempre que a VM é iniciada.

```bash
gcloud compute instances create minha-vm-script \
    --image-family ubuntu-2204-lts \
    --image-project ubuntu-os-cloud \
    --machine-type e2-micro \
    --zone us-central1-a \
    --metadata-from-file startup-script=startup.sh
```

O script `startup.sh` pode conter comandos para instalar pacotes, configurar serviços, etc.

-----

## Opções comuns

  - `--image-family`: A família da imagem do SO (ex: `ubuntu-2204-lts`, `debian-11`).
  - `--image-project`: O projeto que hospeda a família de imagens (ex: `ubuntu-os-cloud`, `debian-cloud`).
  - `--machine-type`: O tipo de máquina da VM (ex: `e2-micro`, `n1-standard-1`).
  - `--zone`: A zona de implantação da VM.
  - `--subnet`: A sub-rede à qual a VM será conectada.
  - `--tags`: Etiquetas de rede para aplicar regras de firewall.
  - `--metadata-from-file`: Fornece o conteúdo de um arquivo para os metadados da instância. Usado com a chave `startup-script` para scripts de inicialização.

## Saída esperada (exemplo)

```json
{
  "creationTimestamp": "2023-10-27T14:30:00.123-07:00",
  "machineType": "https://www.googleapis.com/compute/v1/projects/meu-projeto/zones/us-central1-a/machineTypes/e2-micro",
  "name": "meu-site-vm",
  "networkInterfaces": [
    {
      "network": "https://www.googleapis.com/compute/v1/projects/meu-projeto/global/networks/default",
      "networkIP": "10.128.0.2",
      "accessConfigs": [
        {
          "type": "ONE_TO_ONE_NAT",
          "name": "External NAT",
          "natIP": "34.68.123.45"
        }
      ]
    }
  ],
  "status": "RUNNING",
  "zone": "https://www.googleapis.com/compute/v1/projects/meu-projeto/zones/us-central1-a"
}
```

## Exemplo de criação de uma VM com Ubuntu + Nginx

Este exemplo cria uma VM com Ubuntu, instala o Nginx e cria uma página web simples usando um script de inicialização.

```bash
gcloud compute instances create meu-site-vm \
  --image-family ubuntu-2204-lts \
  --image-project ubuntu-os-cloud \
  --machine-type e2-micro \
  --zone us-central1-a \
  --tags http-server \
  --metadata-from-file startup-script=setup-nginx.sh
```

Exemplo de arquivo `setup-nginx.sh` (os comandos são os mesmos para sistemas baseados em Debian/Ubuntu):

```bash
#!/bin/bash
apt-get update
apt-get install -y nginx
systemctl start nginx
systemctl enable nginx
cat <<EOF > /var/www/html/index.html
<html><body><h1>Site em construção no GCP com Ubuntu</h1></body></html>
EOF
```

Para que o site seja acessível, é necessário criar uma regra de firewall para permitir o tráfego na porta 80.

```bash
gcloud compute firewall-rules create permitir-http --allow tcp:80 --target-tags http-server
```