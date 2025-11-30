# Kubernetes Üzerinde Python & Redis Mimarisi (Stateful)

Bu proje, basit bir Python (Flask) uygulamasını ve Redis veritabanını **Kubernetes (K8s)** üzerinde "Production-Ready" (Canlıya Hazır) bir mimariyle çalıştırmak için tasarlanmıştır.

Proje, klasik Docker Compose yapısından Kubernetes orkestrasyonuna geçişi ve **Stateful (Durumlu)** uygulama yönetimini gösterir.

## Mimari ve Kullanılan Teknolojiler

Bu projede aşağıdaki ileri seviye DevOps pratikleri uygulanmıştır:

* **Ingress Controller:** Uygulamaya `NodePort` (örn: 30005) yerine `http://python-app.local` gibi özel bir domain (alan adı) üzerinden profesyonel erişim sağlandı.
* **Persistent Volume Claim (PVC):** Redis pod'u silinse veya yeniden başlatılsa bile verilerin kaybolmaması için kalıcı disk alanı (Storage) yapılandırıldı.
* **ConfigMap:** `REDIS_HOST` gibi yapılandırma ayarları koddan ayrıştırılarak Kubernetes objesi olarak yönetildi (12-Factor App prensibi).
* **Secrets:** API anahtarları gibi hassas veriler `Kubernetes Secrets` kullanılarak şifreli bir şekilde saklandı.
* **Service Discovery:** Mikroservisler (Python ve Redis) arasındaki iletişim, Kubernetes'in dahili DNS sistemi üzerinden kurgulandı.

## Kurulum ve Çalıştırma

Bu projeyi yerel ortamınızda (Minikube) çalıştırmak için aşağıdaki adımları sırasıyla uygulayın.

### Gereksinimler
* Docker
* Minikube
* Kubectl

### Adım 1: Kümeyi ve Eklentileri Başlatın
Minikube'u başlatın ve Ingress eklentisini aktif hale getirin.
```bash
minikube start --driver=docker
minikube addons enable ingress

### Adım 2: Docker İmajını Oluşturma
# Terminali Minikube'un Docker motoruna bağla
& minikube -p minikube docker-env --shell powershell | Invoke-Expression
# İmajı build et (Sondaki noktayı unutmayın!)
docker build -t python-redis-app:v1 .

### Adım 3: Gizli Anahtarları Oluşturma
kubectl create secret generic my-secret-keys --from-literal=API_KEY=cok_gizli_sifre_123

### Adım 4: Kubernetes Objelerini Uygulama
# 1. Veritabanı Katmanı (Redis + Kalıcı Disk + Servis)
kubectl apply -f k8s/redis-pvc.yaml
kubectl apply -f k8s/redis-deployment.yaml
kubectl apply -f k8s/redis-service.yaml

# 2. Uygulama Katmanı (Python + Ayarlar + Servis)
kubectl apply -f k8s/python-config.yaml
kubectl apply -f k8s/python-deployment.yaml
kubectl apply -f k8s/python-service.yaml

# 3. Ağ Katmanı (Ingress Kapısı)
kubectl apply -f k8s/ingress.yaml

### Adım 5: DNS Ayarı
127.0.0.1 python-app.local