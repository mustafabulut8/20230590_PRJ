"""Urun modeli için birim testleri."""

import unittest
from models.urun import Urun, Elektronik, Giyim, Gida


class TestElektronik(unittest.TestCase):
    """Elektronik ürün sınıfının testleri."""

    def setUp(self):
        """Her test öncesi örnek Elektronik nesnesi oluşturur."""
        self.urun = Elektronik("E001", "Laptop", 15000.0, 10)

    def test_urun_ekle_gecerli_bilgilerle_olusturulur(self):
        """Geçerli parametrelerle ürün başarıyla oluşturulmalıdır."""
        self.assertEqual(self.urun.urun_id, "E001")
        self.assertEqual(self.urun.ad, "Laptop")
        self.assertEqual(self.urun.fiyat, 15000.0)
        self.assertEqual(self.urun.stok, 10)

    def test_urun_listele_kategori_elektronik_doner(self):
        """Elektronik ürünün kategorisi 'Elektronik' olmalıdır."""
        self.assertEqual(self.urun.kategori(), "Elektronik")

    def test_urun_ekle_negatif_fiyat_hata_firlatir(self):
        """Negatif fiyatla oluşturma ValueError fırlatmalıdır."""
        with self.assertRaises(ValueError):
            Elektronik("E002", "Telefon", -100.0, 5)

    def test_urun_ekle_sifir_fiyat_hata_firlatir(self):
        """Sıfır fiyatla oluşturma ValueError fırlatmalıdır."""
        with self.assertRaises(ValueError):
            Elektronik("E003", "Tablet", 0.0, 5)

    def test_urun_ekle_negatif_stok_hata_firlatir(self):
        """Negatif stokla oluşturma ValueError fırlatmalıdır."""
        with self.assertRaises(ValueError):
            Elektronik("E004", "Kamera", 2000.0, -1)

    def test_urun_ekle_kisa_ad_hata_firlatir(self):
        """1 karakterlik adla oluşturma ValueError fırlatmalıdır."""
        with self.assertRaises(ValueError):
            Elektronik("E005", "A", 500.0, 5)

    def test_stok_guncelle_stok_duser(self):
        """Stok güncelleme ile stok miktarı doğru düşmelidir."""
        self.urun.stok_guncelle(-3)
        self.assertEqual(self.urun.stok, 7)

    def test_stok_guncelle_stok_artar(self):
        """Pozitif delta ile stok artmalıdır."""
        self.urun.stok_guncelle(5)
        self.assertEqual(self.urun.stok, 15)

    def test_stok_guncelle_yetersiz_stok_hata_firlatir(self):
        """Stoktan fazla azaltma ValueError fırlatmalıdır."""
        with self.assertRaises(ValueError):
            self.urun.stok_guncelle(-100)

    def test_bilgi_goster_dogru_format(self):
        """bilgi_goster() ID, ad, fiyat ve stok içermelidir."""
        bilgi = self.urun.bilgi_goster()
        self.assertIn("E001", bilgi)
        self.assertIn("Laptop", bilgi)
        self.assertIn("15000.00", bilgi)

    def test_urun_soyut_sinif_dogrudan_olusturulamaz(self):
        """Urun soyut sınıfı doğrudan örneklenememelidir."""
        with self.assertRaises(TypeError):
            Urun("X001", "Test", 100.0, 10)  # type: ignore


class TestGiyim(unittest.TestCase):
    """Giyim ürün sınıfının testleri."""

    def setUp(self):
        """Her test öncesi örnek Giyim nesnesi oluşturur."""
        self.urun = Giyim("G001", "Pantolon", 350.0, 50)

    def test_urun_listele_kategori_giyim_doner(self):
        """Giyim ürününün kategorisi 'Giyim' olmalıdır."""
        self.assertEqual(self.urun.kategori(), "Giyim")

    def test_urun_ekle_gecerli_sifir_stok_kabul_edilir(self):
        """Stok sıfır olarak oluşturulabilmelidir."""
        urun = Giyim("G002", "Gomlek", 200.0, 0)
        self.assertEqual(urun.stok, 0)


class TestGida(unittest.TestCase):
    """Gıda ürün sınıfının testleri."""

    def setUp(self):
        """Her test öncesi örnek Gida nesnesi oluşturur."""
        self.urun = Gida("F001", "Ekmek", 10.0, 100)

    def test_urun_listele_kategori_gida_doner(self):
        """Gıda ürününün kategorisi 'Gida' olmalıdır."""
        self.assertEqual(self.urun.kategori(), "Gida")

    def test_urun_ekle_yanlis_tip_hata_firlatir(self):
        """Fiyat string verilince TypeError fırlatmalıdır."""
        with self.assertRaises(TypeError):
            Gida("F002", "Sut", "ucuz", 50)  # type: ignore
