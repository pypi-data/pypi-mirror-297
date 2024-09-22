from pathlib import Path
from typing import Union

import urllib3
from hvac import Client as Vault
import argparse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

DEFAULT_TOKEN_PATH = Path.home() / ".vault-token"
DEFAULT_VAULT_URL = "https://100.88.114.127:8200"
KV_ENGINE_MOUNT_POINT = "kv"


def print_logo():
    print(r"""
   _____                         _                            __      __         _ _   ______            
  / ____|                       | |                           \ \    / /        | | | |  ____|           
 | |     ___  _ ____   _____  __| | __ _  ___ _ __   ___ ___   \ \  / /_ _ _   _| | |_| |__   _ ____   __
 | |    / _ \| '_ \ \ / / _ \/ _` |/ _` |/ _ \ '_ \ / __/ _ \   \ \/ / _` | | | | | __|  __| | '_ \ \ / /
 | |___| (_) | | | \ V /  __/ (_| | (_| |  __/ | | | (_|  __/    \  / (_| | |_| | | |_| |____| | | \ V / 
  \_____\___/|_| |_|\_/ \___|\__,_|\__, |\___|_| |_|\___\___|     \/ \__,_|\__,_|_|\__|______|_| |_|\_/  
                                    __/ |                                                                
                                   |___/                                                                                  
    """)


def get_vault_token(path: Path):
    with open(path, "r") as f:
        return f.read().strip()


def get_vault_client(token: str, url: str):
    vault = Vault(url, token, timeout=5, verify=False)

    if not vault.is_authenticated():
        raise RuntimeError(
            "Vault client is not authenticated, see "
            "https://www.notion.so/convedgence/bbe8baa0786941808ff0313a035bdd21?v=bc2dc73b84c24afa8f3866000"
            "b49bb26&p=3b0ea14c8f8d4a19afa88a0525271df9&pm=s"
        )

    return vault


def parse_args() -> tuple[str, str, list[str]]:
    parser = argparse.ArgumentParser(description="VaultEnv command line tool")
    parser.add_argument(
        "-p", "--token-path", type=str, help="Path to the vault token file"
    )
    parser.add_argument(
        "-t",
        "--token",
        type=str,
        help="Vault token, if provided --token-path is ignored",
    )
    parser.add_argument("-u", "--vault-url", type=str, help="Vault server URL")
    parser.add_argument(
        "paths",
        nargs="*",
        help="Paths to env files or directories containing a .env file",
    )
    args = parser.parse_args()

    token_path = Path(args.token_path) if args.token_path else DEFAULT_TOKEN_PATH
    token = args.token if args.token else get_vault_token(token_path)
    vault_url = args.vault_url if args.vault_url else DEFAULT_VAULT_URL

    if args.token:
        print(f"→ Using provided token: {args.token[:6]}...{args.token[-6:]}")
    else:
        print(f"→ Using token from {token_path}: {token[:6]}...{token[-6:]}")
    print(f"→ Using vault server URL: {vault_url}")

    return token, vault_url, args.paths


def get_kv_secrets(vault: Vault, path: str):
    secrets = vault.secrets.kv.v2.read_secret_version(
        path, raise_on_deleted_version=True, mount_point=KV_ENGINE_MOUNT_POINT
    )
    return secrets["data"]["data"]


def parse_env_line(line: str) -> tuple[Union[str, None], Union[str, None]]:
    line = line.strip()

    if line and line[0].islower():
        secret_path, secret_key = line.split(".", 1)
        return secret_path, secret_key

    return None, None


def parse_env_content(vault: Vault, content: str) -> str:

    for line in content.split("\n"):
        # Get secret path and key from line
        try:
            secret_path, secret_key = parse_env_line(line)
        except Exception as e:
            print(f"Error parsing line: '{line}', ignoring it. Exception: {e}")
            continue

        if not secret_path or not secret_key:
            continue

        # Fetch secret from vault
        try:
            secret = get_kv_secrets(vault, secret_path)
        except Exception as e:
            print(
                f"Error fetching secret: '{secret_path}', ignoring it. Exception: {e}"
            )
            continue

        # Replace line with secret value(s)
        if secret_key == "*":
            content = content.replace(
                line, "\n".join([f"{k.upper()}={v}" for k, v in secret.items()])
            )
        else:
            if secret_key not in secret:
                print(
                    f"Error: '{secret_key}' not found in secret '{secret_path}', ignoring it."
                )
            else:
                content = content.replace(
                    line, f"{secret_key.upper()}={secret[secret_key]}"
                )

    return content


def main():
    print_logo()
    token, vault_url, paths = parse_args()
    vault = get_vault_client(token, vault_url)

    print("→ Vault client is authenticated.")

    for path in paths:
        # Parse directories
        if path.endswith("/"):
            path = Path(path) / ".env.template"
        else:
            path = Path(path)

        if not path.exists():
            print(f"Error: {path} does not exist, ignoring it.")
        else:
            print(f"→ Parsing file {path}")
            try:
                with open(path, "r") as f:
                    content = f.read()
                parsed_content = parse_env_content(vault, content)

                # Remove eventual .template extension
                if path.suffix == ".template":
                    path = path.with_suffix("")

                with open(path, "w") as f:
                    f.write(parsed_content)
            except Exception as e:
                print(f"Error parsing file: {path}, exception: {e}")


if __name__ == "__main__":
    main()
