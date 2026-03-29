# Detaylı Çözüm

Geliştirilen "Ay İstasyonu" projesi, Ay'ın güney kutbu bölgesinde (87°-90° güney enlemi) görev yapacak otonom bir rover için kapsamlı bir 3D görsel rota planlama aracı sunmaktadır. Bu çözüm, hem büyük topografik verilerin tarayıcıda akıcı bir şekilde işlenmesini hem de yapay zeka destekli görev yönetimini tek bir platformda birleştirir.

## Projenin sunduğu temel çözümler şu başlıklarda toplanabilir:

Büyük Veri Yönetimi ve Görselleştirme: Orijinal boyutu 3.3 GB ve 4.9 GB olan devasa yükseklik (LDEM) ve eğim (LDSM) verileri, sistemin çökmesini engellemek için 10m/px çözünürlüğünde dairesel olarak kırpılarak (yaklaşık 121.4 km çap) optimize edilmiştir. Bu veriler, özel bir sunucu yapısı (HTTP Range Request) sayesinde sadece ihtiyaç duyulan kısımları indirilerek Three.js ile 3D ortamda performanslı bir şekilde oluşturulur.

Otonom ve Güvenli Rota Planlama: Kullanıcı harita üzerinde başlangıç ve bitiş noktalarını seçtiğinde, sistem arka planda 16-yönlü optimize edilmiş bir A* (A-Yıldız) algoritması çalıştırır. Bu çözüm, sadece en kısa mesafeyi değil, aracın devrilmesini önleyecek güvenli eğim sınırlarını ve 90°'den büyük tehlikeli dönüşleri engelleyen fiziksel kısıtlamaları da hesaba katar.

Bilimsel Hedef (Waypoint) Entegrasyonu: Keşif görevleri için Ay yüzeyinde belirlenmiş 8 adet bilimsel odak noktası sisteme tanıtılmıştır. Oluşturulan rota bu noktalara yakınsa sistem kullanıcıyı uyarır ve istenirse hedef noktalarını (waypoint) kapsayacak şekilde, parçalı ve çoklu bir rota optimizasyonu gerçekleştirebilir.

Yapay Zeka Destekli Operasyon: Sadece statik bir harita olmayan bu sistem, Gemini AI (2.0 Flash) entegrasyonu ile akıllı bir görev asistanına dönüşür. Kullanıcılar yapay zeka üzerinden otomatik akademik "Mission Report" (Görev Raporu) alabilir, rotaların güvenliğini analiz ettirebilir veya AI'ın önerdiği farklı bir dönüş güzergahını (turuncu renkli rota) içeren otonom keşif senaryoları çizebilirler.

Simülasyon ve Kullanıcı Deneyimi: Tüm bu sistem; yapay zeka sohbeti, 3D görüntüleyici ve parametre kontrol paneli olmak üzere 3 sütunlu, tek sayfalık pratik bir arayüz (app.html) üzerinden çalışır. Hesaplanıp çizilen rotanın kullanılabilirliği, harita üzerinde hareket eden bir 3D rover modeli (Wall-E) ile üç farklı kamera açısından (serbest, 3. şahıs, 1. şahıs) canlandırılarak test edilir.