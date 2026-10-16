from pathlib import Path

SOURCE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = SOURCE_DIR / "config"

ENV_FILE = CONFIG_DIR / ".env"
CERTIFICATES_DIR = SOURCE_DIR.parent.parent / "certificates"
ROOT_CA_FILE = CERTIFICATES_DIR / "rootCA.pem"
