"""SiparisServisi modülü: Sipariş yönetimi iş mantığını içerir."""

import uuid
from models.siparis import Siparis, SiparisDurumu
from services.urun_servisi import UrunServisi
from services.indirim_stratejisi import SabitYuzdeIndirimi
from utils.logger import Logger


class SiparisServisi:
    """Sipariş oluşturma ve yönetme işlemlerini yürüten servis sınıfı."""

    def __init__(self, urun_servisi: UrunServisi):
        """UrunServisi bağımlılığını constructor ile alır (Dependency Injection)."""
        if not isinstance(urun_servisi, UrunServisi):
            raise TypeError("urun_servisi UrunServisi türünde olmalıdır.")
        self._urun_servisi = urun_servisi
        self._siparisler: dict[str, Siparis] = {}
        self._indirim_stratejisi = SabitYuzdeIndirimi()
        self._logger = Logger()

    def siparis_olustur(self) -> Siparis:
        """Yeni bir sipariş oluşturur ve depoya kaydeder."""
        siparis_id = str(uuid.uuid4())[:8].upper()
        siparis = Siparis(siparis_id)
        self._siparisler[siparis_id] = siparis
        self._logger.bilgi(f"Yeni sipariş oluşturuldu: {siparis_id}")
        return siparis

    def siparis_getir(self, siparis_id: str) -> Siparis:
        """ID'ye göre siparişi döner; bulunamazsa hata fırlatır."""
        if siparis_id not in self._siparisler:
            raise ValueError(f"ID '{siparis_id}' olan sipariş bulunamadı.")
        return self._siparisler[siparis_id]

    def urun_ekle_siparise(self, siparis_id: str, urun_id: str, adet: int):
        """Belirtilen siparişe ürün ekler ve stoktan düşer."""
        siparis = self.siparis_getir(siparis_id)
        urun = self._urun_servisi.urun_getir(urun_id)

        if urun.stok < adet:
            raise ValueError(
                f"Yetersiz stok: '{urun.ad}', mevcut: {urun.stok}, istenen: {adet}"
            )

        siparis.urun_ekle_siparise(urun, adet)
        urun.stok_guncelle(-adet)
        self._logger.bilgi(f"Siparişe ürün eklendi: {urun.ad} x{adet} -> sipariş {siparis_id}")

    def urun_cikar_siparisten(self, siparis_id: str, urun_id: str):
        """Siparişten ürünü çıkarır ve stoğu geri yükler."""
        siparis = self.siparis_getir(siparis_id)
        urun = self._urun_servisi.urun_getir(urun_id)

        mevcut = next(
            (su for su in siparis.urunler if su.urun.urun_id == urun_id), None
        )
        if mevcut is None:
            raise ValueError(f"Ürün '{urun_id}' siparişte bulunamadı.")

        adet = mevcut.adet
        siparis.urun_cikar_siparisten(urun_id)
        urun.stok_guncelle(adet)
        self._logger.bilgi(f"Siparişten ürün çıkarıldı: {urun.ad} -> sipariş {siparis_id}")

    def siparis_tamamla(self, siparis_id: str) -> float:
        """Siparişi otomatik %10 indirimle tamamlar ve indirimli tutarı döner."""
        siparis = self.siparis_getir(siparis_id)
        toplam = siparis.toplam_hesapla()
        indirimli = self._indirim_stratejisi.indirim_uygula(toplam)
        siparis.tamamla(indirimli)
        self._logger.bilgi(
            f"Sipariş tamamlandı: {siparis_id}, orijinal: {toplam:.2f}, indirimli: {indirimli:.2f}"
        )
        return indirimli

    def _stoklari_geri_yukle(self, siparis: Siparis):
        """Siparişdeki tüm ürünlerin stoklarını geri yükler."""
        for su in siparis.urunler:
            su.urun.stok_guncelle(su.adet)

    def siparis_iptal(self, siparis_id: str):
        """Siparişi iptal eder ve stoğu geri yükler."""
        siparis = self.siparis_getir(siparis_id)

        if siparis.durum == SiparisDurumu.TAMAMLANDI:
            raise ValueError("Tamamlanmış sipariş iptal edilemez.")

        self._stoklari_geri_yukle(siparis)
        siparis.iptal_et()
        self._logger.bilgi(f"Sipariş iptal edildi: {siparis_id}")

    def siparis_listele(self) -> list[Siparis]:
        """Tüm siparişlerin listesini döner."""
        return list(self._siparisler.values())
# Siparis servisi
