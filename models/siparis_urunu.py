"""SiparisUrunu modülü: siparisteki bir urunu temsil eder."""

from models.urun import Urun
from utils.dogrulayici import Dogrulayici


class SiparisUrunu:
    """Bir siparişe eklenen ürün ve adet bilgisini kapsüller."""

    def __init__(self, urun: Urun, adet: int):
        """SiparisUrunu nesnesini ürün ve adet ile başlatır."""
        if not isinstance(urun, Urun):
            raise TypeError(f"urun parametresi Urun türünde olmalıdır, alınan: {type(urun).__name__}")
        Dogrulayici.adet_dogrula(adet)

        self._urun = urun
        self._adet = adet

    @property
    def urun(self) -> Urun:
        """İlişkili ürünü döner."""
        return self._urun

    @property
    def adet(self) -> int:
        """Sipariş edilen adeti döner."""
        return self._adet

    def toplam_fiyat(self) -> float:
        """Ürün fiyatı ile adeti çarparak toplam fiyatı hesaplar."""
        return self._urun.fiyat * self._adet

    def bilgi_goster(self) -> str:
        """Siparis urunu bilgilerini formatlı string olarak döner."""
        return (
            f"{self._urun.ad} x{self._adet} = {self.toplam_fiyat():.2f} TL"
        )
# Siparis urunu modeli
