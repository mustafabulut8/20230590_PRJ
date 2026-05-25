"""Urun modülü: Soyut Urun sınıfı ve alt sınıflarını içerir."""

from abc import ABC, abstractmethod
from utils.dogrulayici import Dogrulayici
from utils.logger import Logger


class Urun(ABC):
    """Tüm ürün türleri için soyut temel sınıf."""

    def __init__(self, urun_id: str, ad: str, fiyat: float, stok: int):
        """Ürün temel özelliklerini doğrulayarak başlatır."""
        Dogrulayici.ad_dogrula(ad)
        Dogrulayici.fiyat_dogrula(fiyat)
        Dogrulayici.stok_dogrula(stok)

        self._urun_id = urun_id
        self._ad = ad
        self._fiyat = float(fiyat)
        self._stok = stok
        self._logger = Logger()

    @property
    def urun_id(self) -> str:
        """Ürün ID'sini döner."""
        return self._urun_id

    @property
    def ad(self) -> str:
        """Ürün adını döner."""
        return self._ad

    @property
    def fiyat(self) -> float:
        """Ürün fiyatını döner."""
        return self._fiyat

    @property
    def stok(self) -> int:
        """Ürün stok miktarını döner."""
        return self._stok

    @abstractmethod
    def kategori(self) -> str:
        """Ürün kategorisini döner (alt sınıflar implement eder)."""

    def stok_guncelle(self, miktar: int):
        """Stok miktarını günceller, negatife düşmesini engeller."""
        yeni_stok = self._stok + miktar
        if yeni_stok < 0:
            raise ValueError(
                f"Yetersiz stok. Mevcut: {self._stok}, istenen azalma: {abs(miktar)}"
            )
        self._stok = yeni_stok
        self._logger.bilgi(f"Stok güncellendi: {self._ad}, yeni stok: {self._stok}")

    def bilgi_goster(self) -> str:
        """Ürün bilgilerini formatlı string olarak döner."""
        return (
            f"[{self.kategori()}] ID: {self._urun_id} | "
            f"{self._ad} | Fiyat: {self._fiyat:.2f} TL | Stok: {self._stok}"
        )


class Elektronik(Urun):
    """Elektronik kategorisindeki ürünleri temsil eder."""

    KATEGORI_ADI = "Elektronik"

    def kategori(self) -> str:
        """Elektronik kategorisini döner."""
        return self.KATEGORI_ADI


class Giyim(Urun):
    """Giyim kategorisindeki ürünleri temsil eder."""

    KATEGORI_ADI = "Giyim"

    def kategori(self) -> str:
        """Giyim kategorisini döner."""
        return self.KATEGORI_ADI


class Gida(Urun):
    """Gıda kategorisindeki ürünleri temsil eder."""

    KATEGORI_ADI = "Gida"

    def kategori(self) -> str:
        """Gıda kategorisini döner."""
        return self.KATEGORI_ADI
# Urun modeli
