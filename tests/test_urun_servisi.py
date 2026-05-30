"""UrunServisi ve UrunFactory için birim testleri."""

import unittest
from models.urun import Elektronik, Giyim, Gida
from services.urun_servisi import UrunServisi, UrunFactory


class TestUrunServisi(unittest.TestCase):
    """UrunServisi sınıfının testleri."""

    def setUp(self):
        """Her test öncesi boş bir UrunServisi ve örnek ürünler oluşturur."""
        self.servis = UrunServisi()
        self.urun = Elektronik("E001", "Laptop", 15000.0, 10)

    def test_urun_ekle_basarili(self):
        """Geçerli ürün servise eklenebilmelidir."""
        self.servis.urun_ekle(self.urun)
        self.assertEqual(len(self.servis.urun_listele()), 1)

    def test_urun_ekle_ayni_id_hata_firlatir(self):
        """Aynı ID ile tekrar ekleme ValueError fırlatmalıdır."""
        self.servis.urun_ekle(self.urun)
        urun2 = Elektronik("E001", "Tablet", 5000.0, 5)
        with self.assertRaises(ValueError):
            self.servis.urun_ekle(urun2)

    def test_urun_listele_bos_liste(self):
        """Hiç ürün yokken boş liste dönmelidir."""
        self.assertEqual(self.servis.urun_listele(), [])

    def test_urun_getir_basarili(self):
        """Eklenen ürün ID ile getirilebilmelidir."""
        self.servis.urun_ekle(self.urun)
        getirilen = self.servis.urun_getir("E001")
        self.assertEqual(getirilen.ad, "Laptop")

    def test_urun_getir_olmayan_id_hata_firlatir(self):
        """Olmayan ID ile getirme ValueError fırlatmalıdır."""
        with self.assertRaises(ValueError):
            self.servis.urun_getir("YOKTUR")

    def test_urun_sil_basarili(self):
        """Eklenen ürün silinebilmelidir."""
        self.servis.urun_ekle(self.urun)
        self.servis.urun_sil("E001")
        self.assertEqual(len(self.servis.urun_listele()), 0)

    def test_urun_sil_olmayan_id_hata_firlatir(self):
        """Olmayan ID ile silme ValueError fırlatmalıdır."""
        with self.assertRaises(ValueError):
            self.servis.urun_sil("YOKTUR")

    def test_stok_guncelle_basarili(self):
        """Stok güncelleme doğru çalışmalıdır."""
        self.servis.urun_ekle(self.urun)
        self.servis.stok_guncelle("E001", -3)
        self.assertEqual(self.servis.urun_getir("E001").stok, 7)


class TestUrunFactory(unittest.TestCase):
    """UrunFactory sınıfının testleri."""

    def setUp(self):
        """Her test öncesi bir şey kurulmaz; Factory statik metodlarla çalışır."""
        pass

    def test_urun_olustur_elektronik(self):
        """Factory Elektronik nesnesi üretebilmelidir."""
        urun = UrunFactory.urun_olustur("Elektronik", "E001", "Laptop", 15000.0, 10)
        self.assertIsInstance(urun, Elektronik)

    def test_urun_olustur_giyim(self):
        """Factory Giyim nesnesi üretebilmelidir."""
        urun = UrunFactory.urun_olustur("Giyim", "G001", "Tisort", 150.0, 50)
        self.assertIsInstance(urun, Giyim)

    def test_urun_olustur_gida(self):
        """Factory Gida nesnesi üretebilmelidir."""
        urun = UrunFactory.urun_olustur("Gida", "F001", "Ekmek", 10.0, 100)
        self.assertIsInstance(urun, Gida)

    def test_urun_olustur_gecersiz_kategori_hata_firlatir(self):
        """Geçersiz kategori ValueError fırlatmalıdır."""
        with self.assertRaises(ValueError):
            UrunFactory.urun_olustur("Mobilya", "M001", "Koltuk", 5000.0, 5)
