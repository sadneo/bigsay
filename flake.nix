{
  description = "Python development shell";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-25.11";

  outputs =
    { self, nixpkgs }:
    {
      devShells.x86_64-linux.default =
        let
          pkgs = import nixpkgs {
            system = "x86_64-linux";
          };
        in
        pkgs.mkShell {
          buildInputs = with pkgs; [
            (pkgs.python313.withPackages (python-pkgs: [
              python-pkgs.pygobject3
            ]))
            wrapGAppsHook
            gobject-introspection
            gtk4
          ];
        };
    };
}
