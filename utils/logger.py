"""Logger modülü: Singleton Logger sınıfını içerir."""

import logging


class Logger:
    """Uygulama genelinde tek bir logger örneği sağlayan Singleton sınıfı."""

    _ornek = None
    LOG_FORMATI = "%(asctime)s - %(levelname)s - %(message)s"
    LOG_DOSYASI = "uygulama.log"

    def __new__(cls):
        """Singleton örneğini oluşturur veya mevcut örneği döner."""
        if cls._ornek is None:
            cls._ornek = super().__new__(cls)
            cls._ornek._baslat()
        return cls._ornek

    def _baslat(self):
        """Logger yapılandırmasını başlatır."""
        self._logger = logging.getLogger("UygulamaLogger")
        self._logger.setLevel(logging.DEBUG)

        if not self._logger.handlers:
            self._konsol_handler_ekle()
            self._dosya_handler_ekle()

    def _konsol_handler_ekle(self):
        """Konsol handler ekler."""
        konsol_handler = logging.StreamHandler()
        konsol_handler.setLevel(logging.WARNING)
        konsol_handler.setFormatter(logging.Formatter(self.LOG_FORMATI))
        self._logger.addHandler(konsol_handler)

    def _dosya_handler_ekle(self):
        """Dosya handler ekler."""
        dosya_handler = logging.FileHandler(self.LOG_DOSYASI, encoding="utf-8")
        dosya_handler.setLevel(logging.DEBUG)
        dosya_handler.setFormatter(logging.Formatter(self.LOG_FORMATI))
        self._logger.addHandler(dosya_handler)

    def bilgi(self, mesaj: str):
        """Bilgi seviyesinde log kaydeder."""
        self._logger.info(mesaj)

    def hata(self, mesaj: str):
        """Hata seviyesinde log kaydeder."""
        self._logger.error(mesaj)

    def uyari(self, mesaj: str):
        """Uyarı seviyesinde log kaydeder."""
        self._logger.warning(mesaj)
# Logger singleton
