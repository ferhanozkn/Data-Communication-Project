# Veri İletişimi ve Hata Tespiti Simülasyonu (Socket Programming)
Bu proje, Python ve soket programlama (socket programming) kullanılarak geliştirilmiş bir ağ simülasyonudur. Proje; verinin gönderilmesi, iletim sırasında kasıtlı olarak bozulması (hata enjeksiyonu) ve alıcı tarafta veri bütünlüğünün farklı algoritmalarla kontrol edilmesini (hata tespiti) modeller.

🚀 Proje Mimarisi

Sistem üç ana bileşenden oluşur:

Gönderici (Client Sender): Kullanıcıdan veri alır, seçilen algoritma ile kontrol bitlerini hesaplar ve paketi oluşturur.

Sunucu (Server / Ara Düğüm): Göndericiden gelen paketi alır. "Gürültülü Kanal" rolü üstlenerek veriye kasıtlı hatalar (bit flip, burst error vb.) enjekte eder ve alıcıya iletir.

Alıcı (Client Receiver): Sunucudan gelen paketi alır. Hata kontrol algoritmasını tekrar çalıştırarak gelen verinin bozulup bozulmadığını doğrular.

✨ Özellikler

1. Hata Tespit Algoritmaları (Error Detection Algorithms)
   
    Proje aşağıdaki algoritmaların tamamını destekler:
    
        Parity Bit (Even/Odd): Tek boyutlu eşlik biti kontrolü.
        
        2D Parity: İki boyutlu (satır ve sütun) eşlik kontrolü.
        
        CRC-16: Döngüsel Fazlalık Denetimi (Polynomial: 0x1021).
        
        Hamming Code: Hata tespiti ve düzeltme amaçlı kodlama mantığı.
        
        Internet Checksum: 16-bitlik checksum hesaplaması.

2. Hata Enjeksiyon Yöntemleri (Error Injection)
   
    Server tarafında veriyi bozmak için şu yöntemler kullanılabilir:
    
        Bit Flip: Rastgele bir bitin ters çevrilmesi (0->1, 1->0).
        
        Character Substitution: Bir karakterin rastgele başka bir karakterle değiştirilmesi.
        
        Character Deletion: Veriden bir karakterin silinmesi.
        
        Character Insertion: Araya rastgele bir karakter eklenmesi.
        
        Character Swapping: İki karakterin yer değiştirmesi.
        
        Multiple Bit Flips: Birden fazla bitin aynı anda bozulması.

        Burst Error: Belirli bir aralıktaki verinin tamamen bozulması.

🛠️ Kurulum ve Gereksinimler

Bu proje standart Python kütüphanelerini kullanır, harici bir kurulum gerektirmez.

Dil: Python 3.x

Kütüphaneler: socket, sys, random, time

▶️ Nasıl Çalıştırılır?
Sistemin doğru çalışması için dosyaların sırasıyla ve ayrı terminallerde çalıştırılması gerekir:

Adım 1: Alıcıyı Başlatın
İlk olarak alıcıyı (Receiver) başlatın. Bu, 5001 portunu dinlemeye başlar.


Adım 2: Sunucuyu Başlatın
İkinci terminalde sunucuyu (Server) başlatın. Bu, 5000 portunu dinler ve trafiği yönlendirir.


Adım 3: Göndericiyi Başlatın
Son olarak üçüncü terminalde göndericiyi (Sender) başlatın.


📝 Kullanım Senaryosu

Sender: "Merhaba Dunya" metnini girin ve yöntem olarak "CRC-16"yı seçin.

Sender: Veri paketlenir (Merhaba Dunya|CRC16|<hesaplanan_değer>) ve Server'a gönderilir.

Server: Gelen paketi görür ve size "Hata Enjeksiyon Yöntemi" sorar. Örneğin "Bit Flip" seçin.

Server: Veriyi bozar (Örn: "Merhuba Dunya") ve Receiver'a iletir.

Receiver: Paketi alır. Kendi CRC-16 hesaplamasını yapar. Gelen kontrol kodu ile hesapladığı kodu karşılaştırır.

Sonuç: Kodlar eşleşmediği için ekrana ✗ DATA CORRUPTED (Veri Bozulmuş) yazar.

📂 Dosya Yapısı

client_sender.py: Veri girişi ve kontrol biti hesaplama modülü.

server.py: Veri iletimi ve hata simülasyon modülü (Man-in-the-Middle).

client_receiver.py: Veri doğrulama ve raporlama modülü.

Not: Bu proje eğitim amaçlıdır. Gerçek dünya senaryolarında TCP protokolü zaten kendi hata kontrol mekanizmalarına (Checksum) sahiptir, ancak bu uygulama bu süreçlerin mantığını anlamak için (Application Layer seviyesinde) tasarlanmıştır.

