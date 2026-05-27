"""IndirimStratejisi modülü: Strateji deseni ile indirim hesaplamalarını içerir."""

from abc import ABC, abstractmethod


class IndirimStratejisi(ABC):
    """Tüm indirim stratejileri için soyut temel sınıf."""

    @abstractmethod
    def indirim_uygula(self, toplam: float) -> float:
        """İndirim uygulanmış tutarı hesaplar ve döner."""


class SabitYuzdeIndirimi(IndirimStratejisi):
    """Sabit yüzde üzerinden indirim uygulayan strateji."""

    INDIRIM_YUZDESI = 10

    def indirim_uygula(self, toplam: float) -> float:
        """Toplam tutara %10 indirim uygular."""
        if toplam < 0:
            raise ValueError(f"Toplam tutar negatif olamaz, alınan: {toplam}")
        indirim_orani = self.INDIRIM_YUZDESI / 100
        return toplam * (1 - indirim_orani)
# Indirim stratejisi
# indirim feature branch
