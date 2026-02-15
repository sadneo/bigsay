{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-25.11";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs =
    {
      self,
      nixpkgs,
      flake-utils,
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = import nixpkgs { inherit system; };

        # System dependencies required for GObject/GTK at runtime
        runtimeDeps = with pkgs; [
          gtk4
          pango
          gdk-pixbuf
          gobject-introspection
        ];

        # Build-time dependencies
        buildDeps = with pkgs; [
          pkg-config
          gobject-introspection
        ];
      in
      {
        # The actual package build
        packages.default = pkgs.python3Packages.buildPythonApplication {
          pname = "bigsay";
          version = "0.1.0";
          pyproject = true;
          src = ./.;

          nativeBuildInputs = [ pkgs.wrapGAppsHook4 ] ++ buildDeps;
          buildInputs = runtimeDeps;

          propagatedBuildInputs = with pkgs.python3Packages; [
            pygobject3
          ];
        };

        # The interactive development shell
        devShells.default = pkgs.mkShell {
          packages = [
            pkgs.uv
            pkgs.ruff
          ]
          ++ runtimeDeps
          ++ buildDeps;

          shellHook = ''
            # Create the virtualenv if it doesn't exist
            if [ ! -d ".venv" ]; then
              uv venv
            fi

            # Source the venv so 'python' and 'pip' point to it
            source .venv/bin/activate

            # Ensure uv uses the Nix-provided system libraries for builds
            export LD_LIBRARY_PATH="${pkgs.lib.makeLibraryPath runtimeDeps}"
            export GI_TYPELIB_PATH="${pkgs.lib.makeSearchPath "lib/girepository-1.0" runtimeDeps}"

            echo "BigSay dev environment loaded with 'uv'"
            fish
          '';
        };
      }
    );
}
