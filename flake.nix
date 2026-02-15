{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
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
      in
      {
        packages.default = pkgs.callPackage ./package.nix { };

        devShells.default = pkgs.mkShell {
          nativeBuildInputs = with pkgs; [
            gobject-introspection
            pkg-config
          ];

          buildInputs = with pkgs; [
            gtk4
          ];

          packages = [ pkgs.uv ];

          shellHook = ''
            if [ ! -d ".venv" ]; then
              uv venv
            fi
            source .venv/bin/activate
            uv pip install -e .
          '';
        };
      }
    );
}
