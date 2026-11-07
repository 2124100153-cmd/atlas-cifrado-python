## Requisitos
- Python 3.10+
- Clúster en MongoDB Atlas (7.0 o superior)
- Usuario de base de datos y acceso de red configurado en Atlas

## Instalación (Windows / PowerShell)
```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env   # luego edita .env con tu cadena de conexión
```

## Orden de ejecución
```powershell
python create_collection.py      # colección con JSON Schema
python -c "import os; open('master-key.bin','wb').write(os.urandom(96))"   
python create_data_key.py        # llave de datos (se guarda en .env)
python insert_patient.py         # inserta paciente con campos cifrados
python verify_encryption.py      # national_id y diagnosis salen como Binary
python create_view.py            # vista patients_public con $project
python read_public_view.py       # consulta la vista pública
python test_validation.py        # un documento inválido debe ser rechazado
```

## Seguridad
- `.env` y `master-key.bin` están en `.gitignore` (nunca se suben).
- `national_id`: cifrado determinista (permite búsqueda por igualdad).
- `diagnosis`: cifrado aleatorio (mayor confidencialidad).
- La llave local es solo para pruebas; en producción usar AWS KMS, Azure Key Vault, GCP KMS o KMIP.
- Usuario público con rol personalizado de solo lectura sobre `patients_public`.
- Network Access restringido a las IP necesarias, TLS habilitado, rotar credenciales.

## Evidencias
Capturas en la carpeta `evidencias/`.
