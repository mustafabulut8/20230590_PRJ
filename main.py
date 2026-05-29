"""Ana uygulama modülü: Konsol tabanlı sipariş ve ürün yönetim sistemi."""

from services.urun_servisi import UrunFactory, UrunServisi
from services.siparis_servisi import SiparisServisi
from utils.logger import Logger

ANA_MENU_SECENEKLERI = {
    "1": "Ürün Yönetimi",
    "2": "Sipariş Yönetimi",
    "3": "Çıkış",
}

URUN_MENU_SECENEKLERI = {
    "1": "Ürün Ekle",
    "2": "Ürünleri Listele",
    "3": "Ürün Sil",
    "4": "Geri",
}

SIPARIS_MENU_SECENEKLERI = {
    "1": "Sipariş Oluştur",
    "2": "Siparişe Ürün Ekle",
    "3": "Siparişten Ürün Çıkar",
    "4": "Siparişi Tamamla",
    "5": "Siparişi İptal Et",
    "6": "Siparişleri Listele",
    "7": "Geri",
}

KATEGORILER = ["Elektronik", "Giyim", "Gida"]

URUN_GERI_SECIM = "4"
SIPARIS_GERI_SECIM = "7"
ANA_CIKIS_SECIM = "3"

BASLANGIC_URUNLERI = [
    ("Elektronik", "E001", "Laptop", 15000.0, 10),
    ("Elektronik", "E002", "Telefon", 8000.0, 25),
    ("Elektronik", "E003", "Tablet", 5000.0, 15),
    ("Giyim", "G001", "T-Shirt", 150.0, 100),
    ("Giyim", "G002", "Pantolon", 350.0, 60),
    ("Giyim", "G003", "Ceket", 800.0, 30),
    ("Gida", "F001", "Ekmek", 10.0, 200),
    ("Gida", "F002", "Sut", 25.0, 150),
    ("Gida", "F003", "Peynir", 80.0, 80),
]


def menu_goster(baslik: str, secenekler: dict):
    """Verilen başlık ve seçeneklerle bir menü ekrana basar."""
    print(f"\n{'='*40}")
    print(f"  {baslik}")
    print(f"{'='*40}")
    for anahtar, deger in secenekler.items():
        print(f"  {anahtar}. {deger}")
    print(f"{'='*40}")


def secim_al(prompt: str = "Seçiminiz: ") -> str:
    """Kullanıcıdan string girişi alır."""
    return input(prompt).strip()


def sayi_al(prompt: str) -> int:
    """Kullanıcıdan tam sayı girişi alır; geçersizse hata mesajı verir."""
    try:
        return int(input(prompt).strip())
    except ValueError:
        raise ValueError("Geçerli bir tam sayı giriniz.")


def ondalik_al(prompt: str) -> float:
    """Kullanıcıdan ondalık sayı girişi alır; geçersizse hata mesajı verir."""
    try:
        return float(input(prompt).strip())
    except ValueError:
        raise ValueError("Geçerli bir sayı giriniz.")


def _menu_dongusunu_calistir(baslik: str, secenekler: dict, islemler: dict, cikis_secim: str):
    """Dictionary dispatch ile genel menü döngüsü; cikis_secim gelince sonlanır."""
    while True:
        menu_goster(baslik, secenekler)
        secim = secim_al()
        if secim == cikis_secim:
            break
        islem = islemler.get(secim)
        if islem:
            islem()
        else:
            print("Geçersiz seçim.")


def urunleri_yazdir(urun_servisi: UrunServisi):
    """Tüm ürünleri listeleyerek ekrana basar."""
    urunler = urun_servisi.urun_listele()
    if not urunler:
        print("Kayıtlı ürün bulunmamaktadır.")
        return
    print("\n--- Ürün Listesi ---")
    for urun in urunler:
        print(urun.bilgi_goster())


def urun_ekle_islemi(urun_servisi: UrunServisi, logger: Logger):
    """Kullanıcı girdisiyle yeni ürün oluşturur ve servise ekler."""
    try:
        print("\nKategoriler:", ", ".join(KATEGORILER))
        kategori = secim_al("Kategori: ")
        ad = secim_al("Ürün adı: ")
        fiyat = ondalik_al("Fiyat (TL): ")
        stok = sayi_al("Stok miktarı: ")
        urun_id = secim_al("Ürün ID: ")
        urun = UrunFactory.urun_olustur(kategori, urun_id, ad, fiyat, stok)
        urun_servisi.urun_ekle(urun)
        print(f"Ürün başarıyla eklendi: {urun.bilgi_goster()}")
    except (ValueError, TypeError) as hata:
        logger.hata(str(hata))
        print(f"Hata: {hata}")


def urun_sil_islemi(urun_servisi: UrunServisi, logger: Logger):
    """Kullanıcıdan ID alarak ürünü siler."""
    try:
        urunleri_yazdir(urun_servisi)
        urun_id = secim_al("Silinecek ürün ID: ")
        urun_servisi.urun_sil(urun_id)
        print("Ürün başarıyla silindi.")
    except ValueError as hata:
        logger.hata(str(hata))
        print(f"Hata: {hata}")


def urun_menusu(urun_servisi: UrunServisi, logger: Logger):
    """Ürün yönetimi alt menüsünü dictionary dispatch ile çalıştırır."""
    islemler = {
        "1": lambda: urun_ekle_islemi(urun_servisi, logger),
        "2": lambda: urunleri_yazdir(urun_servisi),
        "3": lambda: urun_sil_islemi(urun_servisi, logger),
    }
    _menu_dongusunu_calistir("Ürün Yönetimi", URUN_MENU_SECENEKLERI, islemler, URUN_GERI_SECIM)


def siparis_olustur_islemi(siparis_servisi: SiparisServisi):
    """Yeni sipariş oluşturur ve ID'yi ekrana basar."""
    siparis = siparis_servisi.siparis_olustur()
    print(f"\nSipariş oluşturuldu! Sipariş ID: {siparis.siparis_id}")


def siparise_urun_ekle_islemi(siparis_servisi: SiparisServisi, urun_servisi: UrunServisi, logger: Logger):
    """Mevcut ürünleri listeledikten sonra siparişe ürün ekler."""
    try:
        urunleri_yazdir(urun_servisi)
        siparis_id = secim_al("Sipariş ID: ")
        urun_id = secim_al("Ürün ID: ")
        adet = sayi_al("Adet: ")
        siparis_servisi.urun_ekle_siparise(siparis_id, urun_id, adet)
        print("Ürün siparişe eklendi.")
    except (ValueError, TypeError) as hata:
        logger.hata(str(hata))
        print(f"Hata: {hata}")


def siparisten_urun_cikar_islemi(siparis_servisi: SiparisServisi, logger: Logger):
    """Siparişten ürün çıkarır."""
    try:
        siparis_id = secim_al("Sipariş ID: ")
        urun_id = secim_al("Çıkarılacak ürün ID: ")
        siparis_servisi.urun_cikar_siparisten(siparis_id, urun_id)
        print("Ürün siparişten çıkarıldı.")
    except ValueError as hata:
        logger.hata(str(hata))
        print(f"Hata: {hata}")


def siparis_tamamla_islemi(siparis_servisi: SiparisServisi, logger: Logger):
    """Siparişi tamamlar ve indirimli tutarı gösterir."""
    try:
        siparis_id = secim_al("Sipariş ID: ")
        indirimli = siparis_servisi.siparis_tamamla(siparis_id)
        print(f"Sipariş tamamlandı! İndirimli toplam: {indirimli:.2f} TL")
    except ValueError as hata:
        logger.hata(str(hata))
        print(f"Hata: {hata}")


def siparis_iptal_islemi(siparis_servisi: SiparisServisi, logger: Logger):
    """Siparişi iptal eder."""
    try:
        siparis_id = secim_al("İptal edilecek sipariş ID: ")
        siparis_servisi.siparis_iptal(siparis_id)
        print("Sipariş iptal edildi.")
    except ValueError as hata:
        logger.hata(str(hata))
        print(f"Hata: {hata}")


def siparisleri_listele_islemi(siparis_servisi: SiparisServisi):
    """Tüm siparişleri listeler."""
    siparisler = siparis_servisi.siparis_listele()
    if not siparisler:
        print("Kayıtlı sipariş bulunmamaktadır.")
        return
    print("\n--- Sipariş Listesi ---")
    for siparis in siparisler:
        print(siparis.bilgi_goster())
        print("-" * 30)


def siparis_menusu(siparis_servisi: SiparisServisi, urun_servisi: UrunServisi, logger: Logger):
    """Sipariş yönetimi alt menüsünü dictionary dispatch ile çalıştırır."""
    islemler = {
        "1": lambda: siparis_olustur_islemi(siparis_servisi),
        "2": lambda: siparise_urun_ekle_islemi(siparis_servisi, urun_servisi, logger),
        "3": lambda: siparisten_urun_cikar_islemi(siparis_servisi, logger),
        "4": lambda: siparis_tamamla_islemi(siparis_servisi, logger),
        "5": lambda: siparis_iptal_islemi(siparis_servisi, logger),
        "6": lambda: siparisleri_listele_islemi(siparis_servisi),
    }
    _menu_dongusunu_calistir("Sipariş Yönetimi", SIPARIS_MENU_SECENEKLERI, islemler, SIPARIS_GERI_SECIM)


def baslangic_verilerini_yukle(urun_servisi: UrunServisi):
    """BASLANGIC_URUNLERI sabitindeki örnek ürünleri sisteme yükler."""
    for kategori, uid, ad, fiyat, stok in BASLANGIC_URUNLERI:
        urun = UrunFactory.urun_olustur(kategori, uid, ad, fiyat, stok)
        urun_servisi.urun_ekle(urun)


def _uygulamayi_kapat(logger: Logger):
    """Çıkış mesajını basar ve kapanış logunu yazar."""
    print("Çıkış yapılıyor. İyi günler!")
    logger.bilgi("Uygulama kapatıldı.")


def main():
    """Uygulamanın ana giriş noktası."""
    logger = Logger()
    urun_servisi = UrunServisi()
    siparis_servisi = SiparisServisi(urun_servisi)

    baslangic_verilerini_yukle(urun_servisi)
    logger.bilgi("Uygulama başlatıldı.")
    print("Sipariş & Ürün Yönetim Sistemi'ne Hoş Geldiniz!")

    islemler = {
        "1": lambda: urun_menusu(urun_servisi, logger),
        "2": lambda: siparis_menusu(siparis_servisi, urun_servisi, logger),
    }
    _menu_dongusunu_calistir("Ana Menü", ANA_MENU_SECENEKLERI, islemler, ANA_CIKIS_SECIM)
    _uygulamayi_kapat(logger)


if __name__ == "__main__":
    main()
