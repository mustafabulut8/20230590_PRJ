"""Entegrasyon testleri: İkili ve üçlü modül birlikte çalışması."""

import unittest
from models.urun import Elektronik, Giyim, Gida
from models.siparis import Siparis, SiparisDurumu
from models.siparis_urunu import SiparisUrunu
from services.urun_servisi import UrunServisi, UrunFactory
from services.siparis_servisi import SiparisServisi
from services.indirim_stratejisi import SabitYuzdeIndirimi


# ── İkili Modül Testleri ──────────────────────────────────────────────────────

class TestSiparisVeSiparisUrunu(unittest.TestCase):
    """Siparis + SiparisUrunu ikili entegrasyon testleri."""

    def setUp(self):
        """Sipariş ve sipariş ürünü nesneleri hazırlanır."""
        self.siparis = Siparis("SP001")
        self.urun = Elektronik("E001", "Laptop", 15000.0, 10)

    def test_siparise_urun_ekle_ve_toplam_hesapla(self):
        """Siparişe eklenen ürünün toplamı doğru hesaplanmalıdır."""
        self.siparis.urun_ekle_siparise(self.urun, 2)
        self.assertAlmostEqual(self.siparis.toplam_hesapla(), 30000.0)

    def test_siparis_urunu_bilgi_goster_dogrulugu(self):
        """SiparisUrunu bilgi gösterimi doğru formatta olmalıdır."""
        su = SiparisUrunu(self.urun, 3)
        bilgi = su.bilgi_goster()
        self.assertIn("Laptop", bilgi)
        self.assertIn("45000.00", bilgi)


class TestUrunVeUrunServisi(unittest.TestCase):
    """Urun + UrunServisi ikili entegrasyon testleri."""

    def setUp(self):
        """Servis ve ürünler hazırlanır; başlangıç ürünü servise eklenir."""
        self.servis = UrunServisi()
        self.urun = Giyim("G001", "Pantolon", 350.0, 20)
        self.servis.urun_ekle(self.urun)

    def test_urun_ekle_ve_stok_guncelle(self):
        """Eklenen ürünün stoğu güncellenebilmelidir."""
        self.servis.stok_guncelle("G001", -5)
        self.assertEqual(self.servis.urun_getir("G001").stok, 15)

    def test_urun_factory_ile_urun_ekle(self):
        """Factory ile oluşturulan ürün servise eklenebilmelidir."""
        urun = UrunFactory.urun_olustur("Gida", "F001", "Ekmek", 10.0, 100)
        self.servis.urun_ekle(urun)
        self.assertEqual(len(self.servis.urun_listele()), 2)


class TestIndirimVeSiparis(unittest.TestCase):
    """IndirimStratejisi + Siparis ikili entegrasyon testleri."""

    def setUp(self):
        """Sipariş ve indirim stratejisi hazırlanır."""
        self.siparis = Siparis("SP002")
        self.urun = Elektronik("E002", "Telefon", 8000.0, 5)
        self.indirim = SabitYuzdeIndirimi()

    def test_indirim_uygula_ve_siparis_tamamla(self):
        """İndirim uygulanarak sipariş tamamlanabilmelidir."""
        self.siparis.urun_ekle_siparise(self.urun, 1)
        toplam = self.siparis.toplam_hesapla()
        indirimli = self.indirim.indirim_uygula(toplam)
        self.siparis.tamamla(indirimli)
        self.assertAlmostEqual(self.siparis.indirimli_toplam, 7200.0)
        self.assertEqual(self.siparis.durum, SiparisDurumu.TAMAMLANDI)


# ── Üçlü Modül Testleri ──────────────────────────────────────────────────────

class TestSiparisServisiUrunServisiIndirim(unittest.TestCase):
    """SiparisServisi + UrunServisi + IndirimStratejisi üçlü entegrasyon testleri."""

    def setUp(self):
        """Tüm servisler ve ürünler hazırlanır."""
        self.urun_servisi = UrunServisi()
        self.siparis_servisi = SiparisServisi(self.urun_servisi)
        self.urun = Elektronik("E001", "Laptop", 10000.0, 5)
        self.urun_servisi.urun_ekle(self.urun)

    def test_tam_siparis_akisi_indirimli_tamamlama(self):
        """Sipariş oluştur → ürün ekle → tamamla akışı %10 indirim uygulamalıdır."""
        siparis = self.siparis_servisi.siparis_olustur()
        self.siparis_servisi.urun_ekle_siparise(siparis.siparis_id, "E001", 2)
        indirimli = self.siparis_servisi.siparis_tamamla(siparis.siparis_id)
        self.assertAlmostEqual(indirimli, 18000.0)
        self.assertEqual(siparis.durum, SiparisDurumu.TAMAMLANDI)

    def test_stok_dogrulugu_ekle_cikar_iptal(self):
        """Ürün ekle, çıkar, iptal döngüsünde stok bütünlüğü korunmalıdır."""
        siparis = self.siparis_servisi.siparis_olustur()
        self.siparis_servisi.urun_ekle_siparise(siparis.siparis_id, "E001", 3)
        self.siparis_servisi.urun_cikar_siparisten(siparis.siparis_id, "E001")
        self.assertEqual(self.urun.stok, 5)
        self.siparis_servisi.siparis_iptal(siparis.siparis_id)
        self.assertEqual(self.urun.stok, 5)


class TestFactoryServisEntegrasyon(unittest.TestCase):
    """UrunFactory + UrunServisi + SiparisServisi üçlü entegrasyon testi."""

    def setUp(self):
        """Factory ile ürün oluşturup servislere bağlar."""
        self.urun_servisi = UrunServisi()
        self.siparis_servisi = SiparisServisi(self.urun_servisi)
        kategoriler = [
            ("Elektronik", "E001", "Laptop", 15000.0, 2),
            ("Giyim", "G001", "Ceket", 800.0, 10),
            ("Gida", "F001", "Peynir", 80.0, 30),
        ]
        for kat, uid, ad, fiyat, stok in kategoriler:
            urun = UrunFactory.urun_olustur(kat, uid, ad, fiyat, stok)
            self.urun_servisi.urun_ekle(urun)

    def test_farkli_kategorilerde_siparis_tamamlama(self):
        """Farklı kategorilerdeki ürünlerle sipariş oluşturulup tamamlanabilmelidir."""
        siparis = self.siparis_servisi.siparis_olustur()
        self.siparis_servisi.urun_ekle_siparise(siparis.siparis_id, "E001", 1)
        self.siparis_servisi.urun_ekle_siparise(siparis.siparis_id, "G001", 2)
        self.siparis_servisi.urun_ekle_siparise(siparis.siparis_id, "F001", 3)
        toplam = 15000.0 + 800.0 * 2 + 80.0 * 3
        indirimli = self.siparis_servisi.siparis_tamamla(siparis.siparis_id)
        self.assertAlmostEqual(indirimli, toplam * 0.9)
