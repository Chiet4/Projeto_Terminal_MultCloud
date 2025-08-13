# Comando para criar um Template de Instância (Instance Template)

## Descrição

Este comando cria um Template de Instância, que é um recurso imutável contendo a configuração completa de uma VM. Templates são a base para a criação de Grupos de Instâncias Gerenciadas (MIGs) e para garantir a consistência ao lançar múltiplas VMs idênticas.

Um template captura o tipo de máquina, imagem, tags, discos e metadados, como scripts de inicialização.

### Comando para criar um template com script de inicialização

Este exemplo cria um template que executa um script no momento da inicialização da VM.

```bash
gcloud compute instance-templates create flask-template \
  --machine-type=e2-micro \
  --image-family ubuntu-2204-lts \
  --image-project ubuntu-os-cloud \
  --tags=flask-vm \
  --metadata-from-file=startup-script:user-data.sh
  --description "Templente minha vm"
```

## Como Atualizar uma Aplicação (Rolling Update)

Uma vez que um template é usado por um Grupo de Instâncias Gerenciadas (MIG), ele não pode ser alterado ou deletado. Para atualizar a configuração das suas VMs (por exemplo, aplicar uma nova versão do seu `user-data.sh`), o processo correto e seguro é o de **"Rolling Update"**.

Este método atualiza as VMs gradualmente, sem tirar sua aplicação do ar.

## O processo consiste em 3 passos:

### **Criar um novo Template com a nova configuração:**
  Dê um nome versionado ao novo template (ex: `flask-template-v2`) para manter a organização.

    ```bash
    gcloud compute instance-templates create flask-template-v2 \
        --machine-type=e2-micro \
        --tags=flask-vm \
        --metadata-from-file startup-script=caminho/para/seu/user-data-v2.sh \
        --image-family=ubuntu-2204-lts \
        --image-project=ubuntu-os-cloud
    ```

### **Iniciar a atualização do Grupo de Instâncias:**
  Instrua o MIG a substituir as VMs antigas por novas, usando o template `v2`.

    ```bash
    gcloud compute instance-groups managed rolling-action start-update [NOME_DO_SEU_MIG] \
        --version=template=flask-template-v2 \
        --zone=[ZONA_DO_SEU_MIG]
    ```

### **(Opcional) Limpar o template antigo:**
    Após a conclusão da atualização e a confirmação de que tudo está funcionando, você pode deletar o template antigo que não está mais em uso.

    ```bash
    gcloud compute instance-templates delete flask-template-v1 --quiet
    ```

## Saída esperada

```json
{
  "creationTimestamp": "2025-07-08T14:35:00.123-03:00",
  "description": "Template para VMs com Flask em Docker",
  "id": "1234567890123456789",
  "kind": "compute#instanceTemplate",
  "name": "flask-template",
  "properties": {
    "disks": [...],
    "machineType": "e2-micro",
    "metadata": { ... },
    "networkInterfaces": [...],
    "tags": {
      "items": [
        "flask-vm"
      ]
    }
  },
  "selfLink": "https://www.googleapis.com/compute/v1/projects/meu-projeto/global/instanceTemplates/flask-template"
}
```

## Opções principais

  * `--machine-type`: O tipo de máquina da VM (ex: `e2-micro`).
  * `--image-family` / `--image`: A imagem de SO a ser utilizada.
  * `--image-project`: O projeto que hospeda a imagem.
  * `--tags`: Uma lista de tags de rede a serem aplicadas.
  * `--metadata` / `--metadata-from-file`: Adiciona metadados à instância, sendo `startup-script` o mais comum para scripts de inicialização.
  * `--description`: Uma descrição textual para o template.