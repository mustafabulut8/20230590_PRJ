"""Sistem testleri: Uçtan uca tam senaryo testleri."""

import unittest
from models.siparis import SiparisDurumu
from services.urun_servisi import UrunFactory, UrunServisi
from services.siparis_servisi import SiparisServisi


def _servis_kur():
    """Test için hazır servis çifti ve 9 ürün döner."""
    urun_servisi = UrunServisi()
    siparis_servisi = SiparisServisi(urun_servisi)
    baslangic = [
        ("Elektronik", "E001", "Laptop", 15000.0, 10),
        ("Elektronik", "E002", "Telefon", 8000.0, 25),
        ("Elektronik", "E003", "Tablet", 5000.0, 15),
        ("Giyim", "G001", "Tisort", 150.0, 100),
        ("Giyim", "G002", "Pantolon", 350.0, 60),
        ("Giyim", "G003", "Ceket", 800.0, 30),
        ("Gida", "F001", "Ekmek", 10.0, 200),
        ("Gida", "F002", "Sut", 25.0, 150),
        ("Gida", "F003", "Peynir", 80.0, 80),
    ]
    for kat, uid, ad, fiyat, stok in baslangic:
        urun = UrunFactory.urun_olustur(kat, uid, ad, fiyat, stok)
        urun_servisi.urun_ekle(urun)
    return urun_servisi, siparis_servisi


class TestTamSiparisSenaryosu(unittest.TestCase):
    """Uçtan uca tam sipariş senaryosu testleri."""

    def setUp(self):
        """Tam sistem kurulumu: 9 ürün yüklü servisler."""
        self.urun_servisi, self.siparis_servisi = _servis_kur()

    def test_senaryo_siparis_olustur_urun_ekle_tamamla(self):
        """Senaryo: sipariş oluştur → ürünler ekle → tamamla → doğrula."""
        siparis = self.siparis_servisi.siparis_olustur()
        sid = siparis.siparis_id

        self.siparis_servisi.urun_ekle_siparise(sid, "E001", 1)
        self.siparis_servisi.urun_ekle_siparise(sid, "G001", 3)
        self.siparis_servisi.urun_ekle_siparise(sid, "F001", 5)

        beklenen_toplam = 15000.0 + 150.0 * 3 + 10.0 * 5
        indirimli = self.siparis_servisi.siparis_tamamla(sid)

        self.assertAlmostEqual(indirimli, beklenen_toplam * 0.9, places=2)
        self.assertEqual(siparis.durum, SiparisDurumu.TAMAMLANDI)
        self.assertEqual(self.urun_servisi.urun_getir("E001").stok, 9)
        self.assertEqual(self.urun_servisi.urun_getir("G001").stok, 97)
        self.assertEqual(self.urun_servisi.urun_getir("F001").stok, 195)

    def test_senaryo_siparis_olustur_urun_ekle_iptal_stok_kontrolu(self):
        """Senaryo: sipariş oluştur → ürün ekle → iptal et → stok sıfırlanır."""
        siparis = self.siparis_servisi.siparis_olustur()
        sid = siparis.siparis_id

        self.siparis_servisi.urun_ekle_siparise(sid, "E002", 5)
        self.siparis_servisi.urun_ekle_siparise(sid, "G002", 10)

        self.assertEqual(self.urun_servisi.urun_getir("E002").stok, 20)
        self.assertEqual(self.urun_servisi.urun_getir("G002").stok, 50)

        self.siparis_servisi.siparis_iptal(sid)

        self.assertEqual(siparis.durum, SiparisDurumu.IPTAL)
        self.assertEqual(self.urun_servisi.urun_getir("E002").stok, 25)
        self.assertEqual(self.urun_servisi.urun_getir("G002").stok, 60)

    def test_senaryo_coklu_siparis_bagimsiz_calisir(self):
        """Senaryo: birden fazla sipariş bağımsız olarak yönetilebilmelidir."""
        s1 = self.siparis_servisi.siparis_olustur()
        s2 = self.siparis_servisi.siparis_olustur()

        self.siparis_servisi.urun_ekle_siparise(s1.siparis_id, "E003", 2)
        self.siparis_servisi.urun_ekle_siparise(s2.siparis_id, "G003", 1)

        self.siparis_servisi.siparis_tamamla(s1.siparis_id)
        self.siparis_servisi.siparis_iptal(s2.siparis_id)

        self.assertEqual(s1.durum, SiparisDurumu.TAMAMLANDI)
        self.assertEqual(s2.durum, SiparisDurumu.IPTAL)
        self.assertEqual(self.urun_servisi.urun_getir("E003").stok, 13)
        self.assertEqual(self.urun_servisi.urun_getir("G003").stok, 30)

    def test_senaryo_urun_sil_sonra_siparise_ekle_hata_firlatir(self):
        """Senaryo: silinen ürün siparişe eklenince ValueError fırlatmalıdır."""
        self.urun_servisi.urun_sil("F003")
        siparis = self.siparis_servisi.siparis_olustur()
        with self.assertRaises(ValueError):
            self.siparis_servisi.urun_ekle_siparise(siparis.siparis_id, "F003", 1)
