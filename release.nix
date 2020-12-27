let
  # start from pinned nixpkgs
  sources = import ./nix/sources.nix {};
  pkgs = import sources.nixpkgs {};

  # TODO detect whether MPI version will work on a given computer and adjust
  raxml  = pkgs.callPackage ./nix/raxml { mpi = true; };

  myPython2 = pkgs.python27Packages // rec {
    fastcluster        = pkgs.python27Packages.callPackage ./nix/pydeps/fastcluster {};
    fasttree           = pkgs.python27Packages.callPackage ./nix/pydeps/fasttree {};
    tree_distance      = pkgs.python27Packages.callPackage ./nix/pydeps/tree_distance {};
    progressbar-latest = pkgs.python27Packages.callPackage ./nix/pydeps/progressbar-latest {};
    CacheControl       = pkgs.python27Packages.callPackage ./nix/pydeps/CacheControl {};
    scikit-bio         = pkgs.python27Packages.callPackage ./nix/pydeps/scikit-bio { inherit CacheControl; };
    phylo_utils        = pkgs.python27Packages.callPackage ./nix/pydeps/phylo_utils {};

    treeCl = pkgs.python27Packages.callPackage ./default.nix {
      inherit raxml; # TODO why doesn't it find this?
      inherit fastcluster fasttree tree_distance progressbar-latest CacheControl scikit-bio phylo_utils;
      inherit (pkgs.python27Packages) pyyaml biopython cython dendropy futures;
      inherit (pkgs.python27Packages) matplotlib nose numpy pandas progressbar scikitlearn scipy;
    };
  };
in
  pkgs.python27Packages.callPackage myPython2.treeCl {}
