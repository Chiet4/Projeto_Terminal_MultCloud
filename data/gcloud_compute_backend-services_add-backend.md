# Comando para Adicionar um Backend a um Serviço de Backend

## Descrição

Este comando é usado para vincular um grupo de instâncias (como um MIG) a um Serviço de Backend existente. Um Serviço de Backend, quando criado, está "vazio", sem destinos para o tráfego. Este comando preenche o serviço com um ou mais backends, tornando-os elegíveis para receber tráfego do Load Balancer.

### Comando para adicionar um MIG como backend

Este comando conecta o `flask-mig` ao `flask-backend` do nosso tutorial.

```bash
gcloud compute backend-services add-backend flask-backend \
  --instance-group flask-mig \
  --instance-group-zone us-central1-a \
  --global
```

## Saída esperada

A saída deste comando é a descrição atualizada do recurso `backend-service`, agora contendo a informação do backend adicionado.

```json
{
  "backends": [
    {
      "balancingMode": "UTILIZATION",
      "capacityScaler": 1.0,
      "group": "https://www.googleapis.com/compute/v1/projects/meu-projeto/zones/us-central1-a/instanceGroups/flask-mig"
    }
  ],
  "creationTimestamp": "2025-07-04T10:08:10.123-03:00",
  "description": "Serviço de backend para o MIG do Flask",
  "healthChecks": [
    "https://www.googleapis.com/compute/v1/projects/meu-projeto/global/healthChecks/flask-health-check"
  ],
  "name": "flask-backend",
  ...
}
```

## Opções principais

  * `--instance-group`: **(Obrigatório)** O nome do grupo de instâncias (gerenciado ou não gerenciado) a ser adicionado.
  * `--instance-group-zone`: A zona do grupo de instâncias, se for um grupo zonal.
  * `--instance-group-region`: A região do grupo de instâncias, se for um grupo regional.
  * `--balancing-mode`: Define como o Load Balancer deve distribuir a carga para este backend (`UTILIZATION`, `RATE`, ou `CONNECTION`).
  * `--global` ou `--region`: Deve corresponder ao escopo do Serviço de Backend que está sendo modificado.