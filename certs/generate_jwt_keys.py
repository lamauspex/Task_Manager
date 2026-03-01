"""Скрипт для генерации JWT ключей"""

from pathlib import Path
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


def generate_jwt_keys():
    """Генерирует JWT ключи если они не существуют."""
    certs_dir = Path(__file__).parent
    private_key_path = certs_dir / "jwt-private.pem"
    public_key_path = certs_dir / "jwt-public.pem"

    # Проверяем существуют ли ключи
    if private_key_path.exists() and public_key_path.exists():
        print("JWT ключи уже существуют.")
        return

    # Генерация приватного ключа
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    # Генерация публичного ключа
    public_key = private_key.public_key()
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Сохранение ключей
    private_key_path.write_bytes(private_pem)
    public_key_path.write_bytes(public_pem)

    print("JWT ключи успешно сгенерированы!")


if __name__ == "__main__":
    generate_jwt_keys()
