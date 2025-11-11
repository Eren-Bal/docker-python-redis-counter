# Docker ile Python (Flask) + Redis Sayaç Projesi

Bu, `docker-compose` kullanılarak oluşturulmuş basit bir "Sayfa Ziyaretçi Sayacı" projesidir.

Backend servisi Python (Flask) kullanır ve sayaç verisini Redis servisinde tutar.

## Kullanılan Teknolojiler

* Python (Flask)
* Redis (Alpine)
* Docker
* Docker Compose

## Nasıl Çalıştırılır?

1.  Repoyu klonlayın: `git clone ...`
2.  Klasöre gidin: `cd docker-python-redis-counter`
3.  Servisleri başlatın: `docker-compose up --build`
4.  Tarayıcınızda `http://localhost:8080` (veya `docker-compose.yml` dosyanızda belirlediğiniz portu) açın.