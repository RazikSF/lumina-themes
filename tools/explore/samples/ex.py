# Seau à jetons : débit limité par seconde
from dataclasses import dataclass

@dataclass
class TokenBucket:
    capacity: float = 10.0
    label: str = "api"

    def try_consume(self, n: int = 1) -> bool:
        if self.tokens < n or n <= 0:
            print(f"vide : {self.tokens}")
            return False
        self.tokens -= n
        return True
