# Comando para criar uma ou mais instâncias EC2 utilizando uma AMI. 

## Descrição
Esse comando é a forma principal de criar uma nova máquina virtual na AWS. Sem fornecer configurações de disco, a AWS automaticamente provisiona um volume EBS padrão com base na AMI usada. Isso cobre a maioria dos casos de uso comuns, como iniciar uma instância Ubuntu com Nginx para servir um site estático.

### Exemplo básico de comando para criar um EC2

```bash
aws ec2 run-instances \
  --image-id ami-07d9b9ddc6cd8dd30 \
  --instance-type t2.micro \
  --security-group-ids <id do seu sg> \
  --key-name <sua key ou vockey> \
  --count 1
```

Este comando:

* Lança 1 instância EC2
* Utiliza a AMI especificada (`<escolha uma ami>`)
* Usa o tipo `t2.micro`
* Atribui grupo de segurança, sub-rede e chave SSH

A AWS automaticamente cria um volume EBS raiz associado.

### Exemplo de comando passando uma sub-net especifica

```bash
aws ec2 run-instances \
  --image-id ami-07d9b9ddc6cd8dd30 \
  --instance-type t2.micro \
  --subnet-id subnet-0123456789abcdef0 \
  --security-group-ids sg-1234567890abcdef0 \
  --key-name <meusite-key ou vockey> \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=vm}]'
```

### Exemplo de comando passando uma sub-net especifica e user data

```bash
aws ec2 run-instances \
  --image-id ami-07d9b9ddc6cd8dd30 \
  --instance-type t2.micro \
  --key-name <sua-chave ou vockey> \
  --security-group-ids sg-xxxxxxxx \
  --subnet-id subnet-a \
  --user-data file://user-data.sh  \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=vm}]'
```

### Exemplo de comando com script de inicialização (User Data)

```bash
aws ec2 run-instances \
  --image-id ami-07d9b9ddc6cd8dd30 \
  --instance-type t2.micro \
  --security-group-ids <id do seu sg> \
  --key-name <sua-chave ou vockey> \
  --user-data file://user-data.sh  \
  --count 1
```

O script `userdata.sh` pode conter comandos como instalação de Nginx, configuração de arquivos HTML, etc.

---

## Opções comuns

* `--image-id`: ID da AMI (ex: Ubuntu, Amazon Linux)
* `--instance-type`: Tipo da máquina (ex: `t2.micro`, `t3.small`)
* `--key-name`: Par de chaves SSH para acesso
* `--security-group-ids`: Um ou mais grupos de segurança
* `--user-data`: Script de inicialização (base64 ou arquivo)
* `--count`: Quantidade de instâncias a iniciar

## Saída esperada (exemplo)

```json
{
  "Instances": [
    {
      "InstanceId": "i-0abcdef1234567890",
      "ImageId": "<id da ami escolhida>",
      "InstanceType": "t2.micro",
      "State": {
        "Name": "pending"
      },
    }
  ]
}
```

## Exemplo de criação de uma instância EC2 com Amazon Linux + Nginx

```bash
aws ec2 run-instances \
  --image-id ami-07d9b9ddc6cd8dd30 \ 
  --count 1 \
  --instance-type t2.micro \
  --key-name <sua-chave ou vockey> \
  --security-group-ids <id do seu sg> \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=meusite-ec2}]' \
  --user-data file://setup-nginx.sh
``` 

Exemplo de arquivo setup-nginx.sh:

```bash
#!/bin/bash
yum update -y
amazon-linux-extras install nginx1 -y
systemctl start nginx
systemctl enable nginx
cd /usr/share/nginx/html
echo "<html><body><h1>Site em construção</h1></body></html>" > index.html
```
