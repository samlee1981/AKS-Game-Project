# AKS 部署指南

這份指南將協助您將 `Game Center` 應用程式部署到 Azure Kubernetes Service (AKS)。

## 前提條件

在開始之前，請確保您的環境中已安裝以下工具：

1.  **Azure CLI (`az`)**: 用於與 Azure 互動。
    - 安裝指南: [Install Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)
2.  **Docker**: 用於建置容器映像檔。
    - 安裝指南: [Install Docker](https://docs.docker.com/get-docker/)
3.  **kubectl**: 用於管理 Kubernetes 叢集。
    - 如果已安裝 Azure CLI，可透過 `az aks install-cli` 安裝。

## 步驟 1: 登入 Azure

在執行部署腳本之前，您必須先登入您的 Azure 帳戶：

```bash
az login
```

這將開啟瀏覽器讓您進行驗證。

## 步驟 2: 執行部署腳本

我們提供了自動化腳本來簡化流程。請根據您的作業系統選擇執行方式：

### Linux / macOS

1.  確保腳本具有執行權限（如果您尚未設定）：
    ```bash
    chmod +x deploy_aks.sh
    ```

2.  執行腳本：
    ```bash
    ./deploy_aks.sh
    ```

### Windows (PowerShell)

1.  開啟 PowerShell。

2.  執行腳本：
    ```powershell
    .\deploy_aks.ps1
    ```

### 腳本執行說明

腳本執行過程中會要求您輸入以下資訊：
    - **Azure Container Registry (ACR) name**: 您的容器登錄名稱（例如 `myacr`，不包含 `.azurecr.io`）。
    - **Resource Group name**: AKS 所在的資源群組名稱。
    - **AKS Cluster name**: 您的 AKS 叢集名稱。

    腳本將會自動執行以下動作：
    - 登入 ACR。
    - 取得 AKS 的存取憑證 (`kubectl` context)。
    - 建置 Docker 映像檔。
    - 推送映像檔至 ACR。
    - 更新 Kubernetes 設定檔並套用至 AKS。

## 步驟 3: 驗證部署

部署完成後，您可以使用以下指令檢查服務狀態：

```bash
kubectl get services
```

您應該會看到 `game-center-lb` 服務，並且在 `EXTERNAL-IP` 欄位顯示一組 IP 位址（如果是 `<pending>` 請稍候幾分鐘）。您可以使用瀏覽器存取該 IP 來測試應用程式。

若要檢查 Pod 的狀態：

```bash
kubectl get pods
```

## 疑難排解

- **Error: Azure CLI is not installed**: 請確認您已安裝 `az` 並加入系統路徑。
- **Login failed**: 如果 ACR 登入失敗，請確認您有足夠的權限，並且 ACR 名稱正確。
- **Pending External IP**: Azure LoadBalancer 分配 IP 可能需要幾分鐘，請耐心等待。
