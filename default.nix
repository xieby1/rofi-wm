{ buildPythonApplication
, pyxdg
, wmctrl
, xprop
, brotab
, kitty
}: buildPythonApplication {
  name = "rofi-wm";
  pyproject = false;
  propagatedBuildInputs = [
    pyxdg
    wmctrl
    xprop
    brotab
    kitty
  ];
  src = ./.;
  installPhase = ''
    mkdir -p $out/bin
    cp ./wm.py $out/bin/
  '';
}
