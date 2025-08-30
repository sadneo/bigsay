{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    (pkgs.python3.withPackages (ps: with ps; [ pygobject3 ]))
    pkgs.gobject-introspection
    pkgs.gtk4
  ];

  shellHook = ''
    exec fish
  '';
}

