import asyncio
import os

from pymongo.encryption import Algorithm

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorClientEncryption


async def main():
    # This must be the same master key that was used to create
    # the encryption key.
    local_master_key = os.urandom(96)
    kms_providers = {"local": {"key": local_master_key}}

    # The MongoDB namespace (db.collection) used to store
    # the encryption data keys.
    key_vault_namespace = "encryption.__pymongoTestKeyVault"
    key_vault_db_name, key_vault_coll_name = key_vault_namespace.split(".", 1)

    # The MotorClient used to read/write application data.
    client = AsyncIOMotorClient()
    coll = client.test.coll
    # Clear old data
    await coll.drop()

    # Set up the key vault (key_vault_namespace) for this example.
    key_vault = client[key_vault_db_name][key_vault_coll_name]
    # Ensure that two data keys cannot share the same keyAltName.
    await key_vault.drop()
    await key_vault.create_index(
        "keyAltNames", unique=True, partialFilterExpression={"keyAltNames": {"$exists": True}}
    )

    client_encryption = AsyncIOMotorClientEncryption(
        kms_providers,
        key_vault_namespace,
        # The Motorlient to use for reading/writing to the key vault.
        # This can be the same MotorClient used by the main application.
        client,
        # The CodecOptions class used for encrypting and decrypting.
        # This should be the same CodecOptions instance you have configured
        # on MotorClient, Database, or Collection.
        coll.codec_options,
    )

    # Create a new data key for the encryptedField.
    data_key_id = await client_encryption.create_data_key(
        "local", key_alt_names=["pymongo_encryption_example_3"]
    )

    # Explicitly encrypt a field:
    encrypted_field = await client_encryption.encrypt(
        "123456789", Algorithm.AEAD_AES_256_CBC_HMAC_SHA_512_Deterministic, key_id=data_key_id
    )
    await coll.insert_one({"encryptedField": encrypted_field})
    doc = await coll.find_one()
    print(f"Encrypted document: {doc}")

    # Explicitly decrypt the field:
    doc["encryptedField"] = await client_encryption.decrypt(doc["encryptedField"])
    print(f"Decrypted document: {doc}")

    # Cleanup resources.
    await client_encryption.close()


if __name__ == "__main__":
    asyncio.run(main())
