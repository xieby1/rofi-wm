let
  pkgs = import <nixpkgs> {};
in pkgs.python3Packages.callPackage ./default.nix {}
