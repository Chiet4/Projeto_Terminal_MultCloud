# Comando para criar um Grupo de Instâncias Gerenciadas (MIG)

## Descrição

Este comando cria um Grupo de Instâncias Gerenciadas (MIG), que é um conjunto de VMs idênticas gerenciadas como uma única entidade. O MIG usa um Template de Instância para criar cada VM, garantindo a uniformidade.

### Comando para criar um MIG

Este comando cria um grupo com 2 instâncias, baseado em um template previamente criado.

```bash
gcloud compute instance-groups managed create flask-mig \
  --base-instance-name flask-vm \
  --template flask-template \
  --size 2 \
  --zone us-central1-a
```

Nota sobre Auto-healing: Para habilitar a funcionalidade de auto-reparo, você deve associar uma verificação de saúde (Health Check) ao grupo. O MIG usará este Health Check para monitorar cada VM e recriar automaticamente aquelas que forem consideradas UNHEALTHY.

### Comando para criar um MIG com Health Check 

```bash
gcloud compute instance-groups managed create flask-mig \
  --base-instance-name flask-vm \
  --template flask-template \
  --size 2 \
  --zone us-central1-a \
  --health-check flask-health-check
```

## Saída esperada

```json
{
  "creationTimestamp": "2025-07-04T10:05:40.123-03:00",
  "baseInstanceName": "flask-vm",
  "id": "1234567890123456789",
  "instanceGroup": "https://www.googleapis.com/compute/v1/projects/meu-projeto/zones/us-central1-a/instanceGroups/flask-mig",
  "instanceTemplate": "https://www.googleapis.com/compute/v1/projects/meu-projeto/global/instanceTemplates/flask-template",
  "name": "flask-mig",
  "targetSize": 2,
  "zone": "https://www.googleapis.com/compute/v1/projects/meu-projeto/zones/us-central1-a"
}
```

## Opções principais

  * `--template`: **(Obrigatório)** O nome do Template de Instância a ser usado.
  * `--size`: **(Obrigatório)** O número de VMs que o grupo deve manter.
  * `--zone` ou `--region`: O escopo do grupo. Use `--zone` para um grupo zonal (padrão) ou `--region` para um MIG regional, que distribui as VMs por múltiplas zonas para maior resiliência.
  * `--base-instance-name`: O prefixo para os nomes das VMs criadas pelo grupo.
