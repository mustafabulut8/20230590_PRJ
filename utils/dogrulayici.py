"""Dogrulayici modülü: Giriş doğrulama static metodlarını içerir."""

MIN_FIYAT = 0.0
MIN_STOK = 0
MIN_ADET = 1
MIN_AD_UZUNLUGU = 2
MAX_AD_UZUNLUGU = 100


class Dogrulayici:
    """Kullanıcı girdilerini ve iş kurallarını doğrulayan yardımcı sınıf."""

    @staticmethod
    def fiyat_dogrula(fiyat: float):
        """Fiyatın geçerli bir pozitif sayı olduğunu doğrular."""
        if not isinstance(fiyat, (int, float)):
            raise TypeError(f"Fiyat sayısal bir değer olmalıdır, alınan: {type(fiyat).__name__}")
        if fiyat <= MIN_FIYAT:
            raise ValueError(f"Fiyat {MIN_FIYAT}'dan büyük olmalıdır, alınan: {fiyat}")

    @staticmethod
    def stok_dogrula(stok: int):
        """Stok miktarının geçerli bir negatif olmayan tam sayı olduğunu doğrular."""
        if not isinstance(stok, int):
            raise TypeError(f"Stok tam sayı olmalıdır, alınan: {type(stok).__name__}")
        if stok < MIN_STOK:
            raise ValueError(f"Stok {MIN_STOK}'dan küçük olamaz, alınan: {stok}")

    @staticmethod
    def ad_dogrula(ad: str):
        """Adın geçerli bir string olduğunu doğrular."""
        if not isinstance(ad, str):
            raise TypeError(f"Ad string olmalıdır, alınan: {type(ad).__name__}")
        ad_temiz = ad.strip()
        if len(ad_temiz) < MIN_AD_UZUNLUGU:
            raise ValueError(f"Ad en az {MIN_AD_UZUNLUGU} karakter olmalıdır, alınan: '{ad}'")
        if len(ad_temiz) > MAX_AD_UZUNLUGU:
            raise ValueError(f"Ad en fazla {MAX_AD_UZUNLUGU} karakter olabilir, alınan: '{ad}'")

    @staticmethod
    def adet_dogrula(adet: int):
        """Adetin geçerli bir pozitif tam sayı olduğunu doğrular."""
        if not isinstance(adet, int):
            raise TypeError(f"Adet tam sayı olmalıdır, alınan: {type(adet).__name__}")
        if adet < MIN_ADET:
            raise ValueError(f"Adet en az {MIN_ADET} olmalıdır, alınan: {adet}")
# Dogrulayici
