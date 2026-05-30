"""Siparis modeli için birim testleri."""

import unittest
from models.siparis import Siparis, SiparisDurumu
from models.urun import Elektronik, Giyim


class TestSiparis(unittest.TestCase):
    """Siparis sınıfının testleri."""

    def setUp(self):
        """Her test öncesi örnek sipariş ve ürünler oluşturur."""
        self.siparis = Siparis("SP001")
        self.urun1 = Elektronik("E001", "Laptop", 15000.0, 10)
        self.urun2 = Giyim("G001", "Tisort", 150.0, 50)

    def test_siparis_olustur_durum_beklemede(self):
        """Yeni sipariş BEKLEMEDE durumunda başlamalıdır."""
        self.assertEqual(self.siparis.durum, SiparisDurumu.BEKLEMEDE)

    def test_siparis_olustur_bos_urun_listesi(self):
        """Yeni sipariş boş ürün listesiyle başlamalıdır."""
        self.assertEqual(len(self.siparis.urunler), 0)

    def test_siparise_urun_ekle_basarili(self):
        """Geçerli ürün siparişe eklenebilmelidir."""
        self.siparis.urun_ekle_siparise(self.urun1, 2)
        self.assertEqual(len(self.siparis.urunler), 1)

    def test_siparise_urun_ekle_ayni_urun_hata_firlatir(self):
        """Aynı ürün tekrar eklenince ValueError fırlatmalıdır."""
        self.siparis.urun_ekle_siparise(self.urun1, 1)
        with self.assertRaises(ValueError):
            self.siparis.urun_ekle_siparise(self.urun1, 1)

    def test_siparisten_urun_cikar_basarili(self):
        """Siparişe eklenen ürün başarıyla çıkarılabilmelidir."""
        self.siparis.urun_ekle_siparise(self.urun1, 1)
        self.siparis.urun_cikar_siparisten("E001")
        self.assertEqual(len(self.siparis.urunler), 0)

    def test_siparisten_urun_cikar_olmayan_urun_hata_firlatir(self):
        """Siparişte olmayan ürün çıkarmaya çalışınca ValueError fırlatmalıdır."""
        with self.assertRaises(ValueError):
            self.siparis.urun_cikar_siparisten("YOKTUR")

    def test_siparis_tamamla_basarili(self):
        """Siparişin durumu TAMAMLANDI olarak güncellenmelidir."""
        self.siparis.urun_ekle_siparise(self.urun1, 1)
        self.siparis.tamamla(13500.0)
        self.assertEqual(self.siparis.durum, SiparisDurumu.TAMAMLANDI)

    def test_siparis_tamamla_bos_siparis_hata_firlatir(self):
        """Boş sipariş tamamlanmaya çalışılınca ValueError fırlatmalıdır."""
        with self.assertRaises(ValueError):
            self.siparis.tamamla(0.0)

    def test_siparis_iptal_et_basarili(self):
        """Beklemedeki sipariş iptal edilebilmelidir."""
        self.siparis.iptal_et()
        self.assertEqual(self.siparis.durum, SiparisDurumu.IPTAL)

    def test_siparis_iptal_et_tamamlandi_hata_firlatir(self):
        """Tamamlanmış sipariş iptal edilince ValueError fırlatmalıdır."""
        self.siparis.urun_ekle_siparise(self.urun1, 1)
        self.siparis.tamamla(13500.0)
        with self.assertRaises(ValueError):
            self.siparis.iptal_et()

    def test_toplam_hesapla_dogru_sonuc(self):
        """Toplam hesaplama doğru tutarı döndürmelidir."""
        self.siparis.urun_ekle_siparise(self.urun1, 2)
        self.siparis.urun_ekle_siparise(self.urun2, 3)
        beklenen = 15000.0 * 2 + 150.0 * 3
        self.assertAlmostEqual(self.siparis.toplam_hesapla(), beklenen)

    def test_bilgi_goster_siparis_id_icerir(self):
        """bilgi_goster() sipariş ID'sini içermelidir."""
        bilgi = self.siparis.bilgi_goster()
        self.assertIn("SP001", bilgi)

    def test_siparis_gecersiz_id_hata_firlatir(self):
        """Boş ID ile sipariş oluşturma ValueError fırlatmalıdır."""
        with self.assertRaises(ValueError):
            Siparis("")
