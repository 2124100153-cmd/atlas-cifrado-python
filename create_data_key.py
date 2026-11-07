import re
import uuid
from bson.codec_options import CodecOptions, UuidRepresentation
from pymongo.encryption import ClientEncryption
from config import get_client, DB_NAME

KEY_VAULT_NAMESPACE = f"{DB_NAME}.__keyVault"


def save_in_env(key_id):
    """Escribe el DATA_KEY_ID en el archivo .env automáticamente."""
    with open(".env", "r", encoding="utf-8") as f:
        content = f.read()
    nueva_linea = f'DATA_KEY_ID="{key_id}"'
    content = re.sub(r'^DATA_KEY_ID=.*$', lambda m: nueva_linea,
                     content, flags=re.MULTILINE)
    with open(".env", "w", encoding="utf-8") as f:
        f.write(content)


def main():
    client = get_client()
    client_encryption = ClientEncryption(
        kms_providers={"local": {"key": open("master-key.bin", "rb").read()}},
        key_vault_namespace=KEY_VAULT_NAMESPACE,
        key_vault_client=client,
        codec_options=CodecOptions(uuid_representation=UuidRepresentation.STANDARD)
    )
    data_key_id = client_encryption.create_data_key(
        "local",
        key_alt_names=["patients-data-key"]
    )
    key_uuid = uuid.UUID(bytes=bytes(data_key_id))
    print("DATA_KEY_ID generado:", key_uuid)
    save_in_env(key_uuid)
    print("Se guardó automáticamente en .env")
    client_encryption.close()
    client.close()


if __name__ == "__main__":
    main()