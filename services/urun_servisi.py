"""UrunServisi modülü: UrunFactory ve UrunServisi sınıflarını içerir."""

from models.urun import Urun, Elektronik, Giyim, Gida
from utils.dogrulayici import Dogrulayici
from utils.logger import Logger


class UrunFactory:
    """Kategori adına göre ürün nesnesi üreten Factory sınıfı."""

    KATEGORILER: dict = {
        Elektronik.KATEGORI_ADI: Elektronik,
        Giyim.KATEGORI_ADI: Giyim,
        Gida.KATEGORI_ADI: Gida,
    }

    @staticmethod
    def urun_olustur(kategori: str, urun_id: str, ad: str, fiyat: float, stok: int) -> Urun:
        """Verilen kategoriye göre uygun Urun alt sınıfını oluşturur."""
        if kategori not in UrunFactory.KATEGORILER:
            gecerli = ", ".join(UrunFactory.KATEGORILER.keys())
            raise ValueError(f"Geçersiz kategori: '{kategori}'. Geçerliler: {gecerli}")
        sinif = UrunFactory.KATEGORILER[kategori]
        return sinif(urun_id, ad, fiyat, stok)


class UrunServisi:
    """Ürün deposunu yöneten servis sınıfı."""

    def __init__(self):
        """Boş ürün deposuyla başlatır."""
        self._urunler: dict[str, Urun] = {}
        self._logger = Logger()

    def urun_ekle(self, urun: Urun):
        """Depoya yeni ürün ekler; aynı ID varsa hata fırlatır."""
        if not isinstance(urun, Urun):
            raise TypeError("Eklenecek nesne Urun türünde olmalıdır.")
        if urun.urun_id in self._urunler:
            raise ValueError(f"ID '{urun.urun_id}' zaten kayıtlı.")
        self._urunler[urun.urun_id] = urun
        self._logger.bilgi(f"Ürün eklendi: {urun.ad} (ID: {urun.urun_id})")

    def urun_getir(self, urun_id: str) -> Urun:
        """ID'ye göre ürünü döner; bulunamazsa hata fırlatır."""
        if urun_id not in self._urunler:
            raise ValueError(f"ID '{urun_id}' olan ürün bulunamadı.")
        return self._urunler[urun_id]

    def urun_sil(self, urun_id: str):
        """Ürünü depodan siler; bulunamazsa hata fırlatır."""
        if urun_id not in self._urunler:
            raise ValueError(f"ID '{urun_id}' olan ürün bulunamadı.")
        ad = self._urunler[urun_id].ad
        del self._urunler[urun_id]
        self._logger.bilgi(f"Ürün silindi: {ad} (ID: {urun_id})")

    def urun_listele(self) -> list[Urun]:
        """Depodaki tüm ürünlerin listesini döner."""
        return list(self._urunler.values())

    def stok_guncelle(self, urun_id: str, miktar: int):
        """Verilen ID'li ürünün stok miktarını günceller."""
        Dogrulayici.stok_dogrula(abs(miktar))
        urun = self.urun_getir(urun_id)
        urun.stok_guncelle(miktar)
        self._logger.bilgi(f"Stok güncellendi: {urun.ad}, delta: {miktar}")
# Urun servisi
