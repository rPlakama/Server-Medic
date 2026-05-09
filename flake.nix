{
  description = "Server_medic - Plataforma de distribuicao de conteudos medicos";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        python = pkgs.python313;
      in
      {
        devShells.default = pkgs.mkShell {
          packages = with pkgs; [
            python
            python.pkgs.pip
            python.pkgs.virtualenv
            podman
            mariadb-connector-c
            gcc
            pkg-config
            zlib
            openssl
            git
          ];

          env = {
            DB_HOST = "127.0.0.1";
            DB_PORT = "3306";
            DB_NAME = "server_medic";
            DB_USER = "medic";
            DB_PASSWORD = "medicpass";
            LD_LIBRARY_PATH = "${pkgs.lib.makeLibraryPath [pkgs.mariadb-connector-c]}";
          };

          shellHook = ''
            echo "=== Server_medic devshell ==="

            export DB_HOST=127.0.0.1
            export DB_PORT=3306
            export DB_NAME=server_medic
            export DB_USER=medic
            export DB_PASSWORD=medicpass

            # Ensure podman policy.json exists (required on non-NixOS)
            POLICY_DIRS=( "$HOME/.config/containers" "/etc/containers" )
            POLICY_FOUND=false
            for d in "''${POLICY_DIRS[@]}"; do
              if [ -f "$d/policy.json" ]; then
                POLICY_FOUND=true
                break
              fi
            done
            if [ "$POLICY_FOUND" = false ]; then
              mkdir -p "$HOME/.config/containers"
              cat > "$HOME/.config/containers/policy.json" <<'POLICY'
            {
              "default": [
                {
                  "type": "insecureAcceptAnything"
                }
              ]
            }
            POLICY
              echo "Created podman policy.json at $HOME/.config/containers/policy.json"
            fi

            # Ensure podman registries.conf exists
            if [ ! -f "$HOME/.config/containers/registries.conf" ] && [ ! -f "/etc/containers/registries.conf" ]; then
              mkdir -p "$HOME/.config/containers"
              cat > "$HOME/.config/containers/registries.conf" <<'REGISTRIES'
            [registries.search]
            registries = ['docker.io']

            [registries.insecure]
            registries = []

            [registries.block]
            registries = []
            REGISTRIES
              echo "Created podman registries.conf"
            fi

            # Start podman socket if using rootless
            if [ -n "''${XDG_RUNTIME_DIR:-}" ] && [ ! -S "$XDG_RUNTIME_DIR/podman/podman.sock" ]; then
              podman system service --time=0 &>/dev/null &
              sleep 1
            fi

            if [ ! -d ".venv" ]; then
              echo "Creating Python virtual environment..."
              python -m venv .venv
              source .venv/bin/activate
              pip install --upgrade pip
              pip install -r requirements.txt
            else
              source .venv/bin/activate
            fi

            if ! podman ps --format '{{.Names}}' 2>/dev/null | grep -q '^medic_db$'; then
              if podman ps -a --format '{{.Names}}' 2>/dev/null | grep -q '^medic_db$'; then
                echo "Starting existing MariaDB container..."
                podman start medic_db
              else
                echo "Creating MariaDB container..."
                podman run -d \
                  --name medic_db \
                  -e MARIADB_ROOT_PASSWORD=rootpass \
                  -e MARIADB_DATABASE=server_medic \
                  -e MARIADB_USER=medic \
                  -e MARIADB_PASSWORD=medicpass \
                  -p 3306:3306 \
                  docker.io/library/mariadb:11
              fi
              echo "Waiting for MariaDB to accept connections..."
              for i in $(seq 1 60); do
                if podman exec medic_db mariadb -u medic -pmedicpass -e "SELECT 1" &>/dev/null; then
                  echo "MariaDB is ready."
                  break
                fi
                if [ $i -eq 60 ]; then
                  echo "WARNING: MariaDB did not become ready within 60s."
                fi
                sleep 1
              done
            else
              echo "MariaDB container is already running."
            fi

            echo ""
            echo "MariaDB: $DB_USER@localhost:$DB_PORT/$DB_NAME"
            echo "Run 'python manage.py migrate' to apply migrations."
          '';
        };
      });
}