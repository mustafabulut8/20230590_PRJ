"""SiparisServisi için birim testleri."""

import unittest
from models.urun import Elektronik, Giyim
from services.urun_servisi import UrunServisi
from services.siparis_servisi import SiparisServisi
from models.siparis import SiparisDurumu


class TestSiparisServisi(unittest.TestCase):
    """SiparisServisi sınıfının testleri."""

    def setUp(self):
        """Her test öncesi servisler ve ürünler oluşturulur."""
        self.urun_servisi = UrunServisi()
        self.servis = SiparisServisi(self.urun_servisi)

        self.urun1 = Elektronik("E001", "Laptop", 15000.0, 10)
        self.urun2 = Giyim("G001", "Tisort", 150.0, 50)
        self.urun_servisi.urun_ekle(self.urun1)
        self.urun_servisi.urun_ekle(self.urun2)

    def test_siparis_olustur_basarili(self):
        """Sipariş oluşturulabilmelidir."""
        siparis = self.servis.siparis_olustur()
        self.assertIsNotNone(siparis.siparis_id)

    def test_siparis_olustur_listede_gorunur(self):
        """Oluşturulan sipariş listede görünmelidir."""
        self.servis.siparis_olustur()
        self.assertEqual(len(self.servis.siparis_listele()), 1)

    def test_siparise_urun_ekle_basarili(self):
        """Servisten siparişe ürün eklenebilmelidir."""
        siparis = self.servis.siparis_olustur()
        self.servis.urun_ekle_siparise(siparis.siparis_id, "E001", 2)
        self.assertEqual(len(siparis.urunler), 1)

    def test_siparise_urun_ekle_stok_duser(self):
        """Siparişe eklenen ürünün stoğu düşmelidir."""
        siparis = self.servis.siparis_olustur()
        self.servis.urun_ekle_siparise(siparis.siparis_id, "E001", 3)
        self.assertEqual(self.urun1.stok, 7)

    def test_siparise_urun_ekle_yetersiz_stok_hata_firlatir(self):
        """Stoktan fazla adet eklenince ValueError fırlatmalıdır."""
        siparis = self.servis.siparis_olustur()
        with self.assertRaises(ValueError):
            self.servis.urun_ekle_siparise(siparis.siparis_id, "E001", 100)

    def test_siparis_tamamla_indirim_uygulanir(self):
        """Tamamlama %10 indirim uygulamalıdır."""
        siparis = self.servis.siparis_olustur()
        self.servis.urun_ekle_siparise(siparis.siparis_id, "E001", 1)
        indirimli = self.servis.siparis_tamamla(siparis.siparis_id)
        self.assertAlmostEqual(indirimli, 15000.0 * 0.9)

    def test_siparis_tamamla_durum_degisir(self):
        """Tamamlanan siparişin durumu TAMAMLANDI olmalıdır."""
        siparis = self.servis.siparis_olustur()
        self.servis.urun_ekle_siparise(siparis.siparis_id, "E001", 1)
        self.servis.siparis_tamamla(siparis.siparis_id)
        self.assertEqual(siparis.durum, SiparisDurumu.TAMAMLANDI)

    def test_siparis_iptal_durum_degisir(self):
        """İptal edilen siparişin durumu IPTAL olmalıdır."""
        siparis = self.servis.siparis_olustur()
        self.servis.siparis_iptal(siparis.siparis_id)
        self.assertEqual(siparis.durum, SiparisDurumu.IPTAL)

    def test_siparis_iptal_stok_geri_yukselir(self):
        """İptal edilince ürün stoğu geri yüklenmelidir."""
        siparis = self.servis.siparis_olustur()
        self.servis.urun_ekle_siparise(siparis.siparis_id, "E001", 3)
        self.servis.siparis_iptal(siparis.siparis_id)
        self.assertEqual(self.urun1.stok, 10)

    def test_siparisten_urun_cikar_stok_geri_yukselir(self):
        """Siparişten çıkarılan ürünün stoğu geri yüklenmelidir."""
        siparis = self.servis.siparis_olustur()
        self.servis.urun_ekle_siparise(siparis.siparis_id, "G001", 5)
        self.servis.urun_cikar_siparisten(siparis.siparis_id, "G001")
        self.assertEqual(self.urun2.stok, 50)
