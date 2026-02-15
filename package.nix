{ lib
, python3Packages
, gtk4
, gobject-introspection
, pkg-config
, wrapGAppsHook4
}:

python3Packages.buildPythonApplication {
  pname = "bigsay";
  version = "0.1.0";
  pyproject = true;

  src = ./.;

  nativeBuildInputs = [
    pkg-config
    gobject-introspection
    wrapGAppsHook4
    python3Packages.hatchling
  ];

  buildInputs = [
    gtk4
  ];

  propagatedBuildInputs = with python3Packages; [
    pygobject3
  ];

  meta = with lib; {
    description = "GTK4 text display tool";
    license = licenses.mit;
    mainProgram = "bigsay";
  };
}
