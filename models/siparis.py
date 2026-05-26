"""Siparis modülü: SiparisDurumu Enum ve Siparis sınıfını içerir."""

from enum import Enum
from models.siparis_urunu import SiparisUrunu
from models.urun import Urun
from utils.logger import Logger


class SiparisDurumu(Enum):
    """Siparişin olası durumlarını tanımlar."""

    BEKLEMEDE = "Beklemede"
    TAMAMLANDI = "Tamamlandı"
    IPTAL = "İptal"


class Siparis:
    """Bir müşteri siparişini ve içerdiği ürünleri yönetir."""

    def __init__(self, siparis_id: str):
        """Siparis nesnesini ID ile başlatır."""
        if not siparis_id or not isinstance(siparis_id, str):
            raise ValueError("Sipariş ID geçerli bir string olmalıdır.")

        self._siparis_id = siparis_id
        self._urunler: list[SiparisUrunu] = []
        self._durum = SiparisDurumu.BEKLEMEDE
        self._indirimli_toplam: float | None = None
        self._logger = Logger()

    @property
    def siparis_id(self) -> str:
        """Sipariş ID'sini döner."""
        return self._siparis_id

    @property
    def urunler(self) -> list:
        """siparis urunlerinin kopyasini döner."""
        return list(self._urunler)

    @property
    def durum(self) -> SiparisDurumu:
        """Siparişin mevcut durumunu döner."""
        return self._durum

    @property
    def indirimli_toplam(self) -> float | None:
        """Uygulanan indirimli toplam fiyatı döner."""
        return self._indirimli_toplam

    def urun_ekle_siparise(self, urun: Urun, adet: int):
        """Siparişe ürün ekler; durum BEKLEMEDE değilse hata fırlatır."""
        if self._durum != SiparisDurumu.BEKLEMEDE:
            raise ValueError(f"'{self._durum.value}' durumundaki siparişe ürün eklenemez.")

        mevcut = self._urun_bul(urun.urun_id)
        if mevcut is not None:
            raise ValueError(f"'{urun.ad}' zaten siparişte mevcut. Önce çıkarın.")

        siparis_urunu = SiparisUrunu(urun, adet)
        self._urunler.append(siparis_urunu)
        self._logger.bilgi(f"Siparişe ürün eklendi: {urun.ad} x{adet}")

    def urun_cikar_siparisten(self, urun_id: str):
        """Siparişten ürünü çıkarır; bulunamazsa hata fırlatır."""
        if self._durum != SiparisDurumu.BEKLEMEDE:
            raise ValueError(f"'{self._durum.value}' durumundaki siparişten ürün çıkarılamaz.")

        mevcut = self._urun_bul(urun_id)
        if mevcut is None:
            raise ValueError(f"ID '{urun_id}' olan ürün siparişte bulunamadı.")

        self._urunler.remove(mevcut)
        self._logger.bilgi(f"Siparişten ürün çıkarıldı: {mevcut.urun.ad}")

    def _urun_bul(self, urun_id: str) -> SiparisUrunu | None:
        """Verilen ID'ye sahip sipariş ürününü döner, yoksa None döner."""
        for siparis_urunu in self._urunler:
            if siparis_urunu.urun.urun_id == urun_id:
                return siparis_urunu
        return None

    def toplam_hesapla(self) -> float:
        """Siparişin indirim uygulanmamış toplam tutarını hesaplar."""
        return sum(su.toplam_fiyat() for su in self._urunler)

    def tamamla(self, indirimli_tutar: float):
        """Siparişi tamamlar ve indirimli tutarı kaydeder."""
        if self._durum != SiparisDurumu.BEKLEMEDE:
            raise ValueError(f"Sipariş zaten '{self._durum.value}' durumunda.")
        if not self._urunler:
            raise ValueError("Boş sipariş tamamlanamaz.")

        self._indirimli_toplam = indirimli_tutar
        self._durum = SiparisDurumu.TAMAMLANDI
        self._logger.bilgi(f"Sipariş tamamlandı: {self._siparis_id}")

    def iptal_et(self):
        """Siparişi iptal eder; zaten tamamlandıysa hata fırlatır."""
        if self._durum == SiparisDurumu.TAMAMLANDI:
            raise ValueError("Tamamlanmış sipariş iptal edilemez.")
        if self._durum == SiparisDurumu.IPTAL:
            raise ValueError("Sipariş zaten iptal edilmiş.")

        self._durum = SiparisDurumu.IPTAL
        self._logger.bilgi(f"Sipariş iptal edildi: {self._siparis_id}")

    def bilgi_goster(self) -> str:
        """Sipariş bilgilerini formatlı string olarak döner."""
        satirlar = [f"Sipariş ID: {self._siparis_id} | Durum: {self._durum.value}"]
        for su in self._urunler:
            satirlar.append(f"  - {su.bilgi_goster()}")
        satirlar.append(f"  Ara Toplam: {self.toplam_hesapla():.2f} TL")
        if self._indirimli_toplam is not None:
            satirlar.append(f"  İndirimli Toplam: {self._indirimli_toplam:.2f} TL")
        return "\n".join(satirlar)
# Siparis modeli
