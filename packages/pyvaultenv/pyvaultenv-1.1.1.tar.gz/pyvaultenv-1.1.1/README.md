# VaultEnv

A simple script to pull env vars from hashicorp vault for developers

## Install & configure

Install the app using:
```bash
pip install git+ssh://git@github.com/Convedgence/VaultEnv.git
```

Follow the [vault cli setup instructions](https://www.notion.so/convedgence/bbe8baa0786941808ff0313a035bdd21?v=bc2dc73b84c24afa8f3866000b49bb26&p=3b0ea14c8f8d4a19afa88a0525271df9&pm=s) to setup your vault cli

## Usage

Run `vault-env -h` to see the help menu

### Basic usage

Run the `vault-env` command followed by as many paths as you want to parse the env files.

Paths you provide should either be a path to a folder containing a `.env.template` file or a path to an env template file.

e.g. 
```bash
vault-env ./folder_containing_.env_file/ ./.custom_env_file
```

### Creating env files template

In your .env file template, you can specify either:
- A static env var, the key should be uppercase. `<ENV_VAR_NAME>=<ENV_VAR_VALUE>`
- A vault secret path, the key should be lowercase. `<vault_secret_path>.<vault_secret_key_or_wildcard>`

e.g.
```env
MY_STATIC_VAR=static_value
developer/my_secret.secret_key
developer/my_other_secret.*
```

### Custom token & url

The default URL for the vault server is set on the tailscaile IP.
The default vault token dir is set to `~/.vault-token`, this is the default location used by the vault cli.

If you really need to change these values, use the `--vault-url` and `--token-path` flags.
For example:
```bash
vault-env --vault-url http://my_vault:8200 --token-path ~/.my_vault_token
```

If you want you can directly specify the token in the command line using the `--token` flag.
