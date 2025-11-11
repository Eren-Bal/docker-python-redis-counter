from flask import Flask
from redis import Redis, RedisError
import os

# Flask uygulamasını başlat
app = Flask(__name__)

# Redis'e bağlan
# Tıpkı Postgres'te olduğu gibi, host adını bir ortam değişkeninden (env var) alıyoruz.
# Eğer değişken ayarlanmamışsa, varsayılan olarak 'redis' (servis adı) kullanılacak.
redis_host = os.environ.get('REDIS_HOST', 'redis')

try:
    # 'decode_responses=True' string olarak sonuç almamızı sağlar
    redis = Redis(host=redis_host, port=6379, decode_responses=True)
except RedisError:
    print("Redis sunucusuna bağlanılamadı.")
    redis = None

@app.route('/')
def hello():
    if redis:
        try:
            # 'counter' adındaki değeri 1 artır ve yeni değeri al
            count = redis.incr('counter')
            return f'Bu sayfa {count} kez ziyaret edildi.'
        except RedisError:
            return 'Veritabanına (Redis) bağlanırken bir hata oluştu.'
    else:
        return 'Redis bağlantısı kurulamadı.'

if __name__ == "__main__":
    # Container içinde dışarıdan erişim için 0.0.0.0
    app.run(host="0.0.0.0", port=8080, debug=True)