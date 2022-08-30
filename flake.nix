{
  inputs = {
    flake-utils = {
      url = "github:numtide/flake-utils";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, flake-utils, ... }:
    (flake-utils.lib.eachDefaultSystem
      (system:
        let
          pkgs = import nixpkgs { inherit system; };
        in
        {
          devShell = pkgs.mkShell {
            buildInputs = with pkgs; [
              python3
              python3Packages.requests
              python3Packages.selenium
              python3Packages.beautifulsoup4
            ];
          };
        }))
  ;
}
