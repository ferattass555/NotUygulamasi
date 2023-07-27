# Not Tutma Uygulaması

Bu, Python'da PyQt5 kullanılarak geliştirilmiş basit bir not tutma uygulamasıdır. Kullanıcılar belirli tarih ve saatlere sahip notlar oluşturabilir, görüntüleyebilir, güncelleyebilir ve silebilirler.

## Özellikler

- Yeni notlar oluşturma: Kullanıcılar "Not" metin alanına içerik girerek, takvim ve saat seçimleriyle birlikte yeni notlar oluşturabilirler.

- Notları listeleme: Kullanıcılar "Notları Göster" düğmesine tıklayarak tüm kaydedilmiş notların listesini görüntüleyebilirler.

- Notları güncelleme: Kullanıcılar notları listesinden bir not seçerek "Güncelle" düğmesine tıklayarak not içeriğini güncelleyebilirler.

- Notları silme: Kullanıcılar notları listesinden bir not seçerek "Sil" düğmesine tıklayarak notları silebilirler.

- Hatırlatıcılar: Uygulama, her dakika hatırlatıcıları kontrol eder ve bir notun belirtilen tarih ve saatine ulaştıysa kullanıcıya hatırlatıcı mesajı gösterir.

- Notların dosyada kaydedilmesi: Oluşturulan notlar "not.txt" adlı bir dosyada saklanır ve uygulama başlatıldığında bu dosyadan notlar yüklenir.

## Gereksinimler

- Python 3.x
- PyQt5

## Nasıl Kullanılır

1. Uygulamayı çalıştırın: Terminal veya komut satırında aşağıdaki komutu girin:

python not_tutma_uygulamasi.py


2. Uygulama penceresi açılacaktır. "Not" metin alanına içerik yazın, takvim kullanarak bir tarih seçin ve saat girişiyle bir saat belirleyin.

3. Notu kaydetmek için "Kaydet" düğmesine tıklayın.

4. Kaydedilen notları görmek için "Notları Göster" düğmesine tıklayın. Yeni bir pencere açılacak ve tüm notların bir listesini gösterecektir.

5. Listede bir notu çift tıklayarak, notun içeriğini içeren bir metin dosyasını açabilirsiniz.

6. Bir notu güncellemek veya silmek için listeden notu seçip "Güncelle" veya "Sil" düğmesine tıklayın.

7. Uygulama her dakika için hatırlatıcıları kontrol edecektir. Eğer bir hatırlatıcı zamanı gelmişse, uygulama penceresinin başlığı hatırlatmayı belirtmek için değişecektir.

8. Uygulamadan çıkmak için ana pencereyi kapatın.

## Notlar

- Notlar, "not.txt" adlı bir dosyada uygulama ile aynı dizinde kaydedilir. Her notun verileri şu formatta kaydedilir: "index|tarih_saat|icerik".

- Uygulama, hatırlatıcıları sistemin tarih ve saati üzerinden kontrol eder. Doğru hatırlatmalar almak için sisteminizin tarih ve saat ayarlarının doğru olduğundan emin olun.

## Yazar

Bu uygulama [Adınız] tarafından oluşturulmuştur.

## Lisans

Bu proje MIT Lisansı altında lisanslanmıştır. Özgürce kullanabilir ve değiştirebilirsiniz.
