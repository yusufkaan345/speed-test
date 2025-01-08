# Speed Test Monitör

## Kurulum

1. Repoyu klonlayın

2. Gerekli paketleri yükleyin: pip install -r requirements.txt

3. E-posta yapılandırması:
   - İlk çalıştırmada uygulama sizden e-posta bilgilerini isteyecektir
   - Gmail kullanıyorsanız, "App Password" oluşturmanız gerekir:
     1. Google Hesabınıza gidin
     2. Güvenlik > 2 Adımlı Doğrulama'yı açın
     3. Uygulama Şifreleri'nden yeni bir şifre oluşturun
     4. Bu şifreyi kullanarak e-posta bilgilerini girin
     5.Bu bilgiler kendi bilgisayarınızda saklanacaktır endişelenmeyin.

4. Docker ile çalıştırma:
   .env dosyasını oluşturun
    cp .env.example .env
   .env dosyasını düzenleyin
    Docker compose ile başlatın
    docker-compose up -d

5. Uygulama başlatıldığında, her saatte bir hız testi yapılacaktır

6. Hız testi sonuçları speedtest_results.json dosyasına kaydedilecektir

7. Eğer hız testi sonucu belirli bir eşiği altına düşerse, e-posta bildirimi gönderilecektir.

## Güvenlik Notları

- .env dosyasını asla GitHub'a push etmeyin
