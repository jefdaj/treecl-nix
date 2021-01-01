let
  # start from pinned nixpkgs
  sources = import ./nix/sources.nix {};
  pkgs = import sources.nixpkgs {};

  # TODO detect whether MPI version will work on a given computer and adjust
  # TODO is this messing up the build?
  raxml  = pkgs.callPackage sources.raxml { mpi = true; };

  # TODO there's probably a withPackages function for this right?
  myPython2 = pkgs.python27Packages // rec {
    fastcluster        = pkgs.python27Packages.callPackage ./nix/pydeps/fastcluster {};
    fasttree           = pkgs.python27Packages.callPackage ./nix/pydeps/fasttree {};
    tree_distance      = pkgs.python27Packages.callPackage ./nix/pydeps/tree_distance {};
    progressbar-latest = pkgs.python27Packages.callPackage ./nix/pydeps/progressbar-latest {};
    CacheControl       = pkgs.python27Packages.callPackage ./nix/pydeps/CacheControl {};
    phylo_utils        = pkgs.python27Packages.callPackage ./nix/pydeps/phylo_utils {};
    biopython          = pkgs.python27Packages.callPackage ./nix/pydeps/biopython {};
    natsort            = pkgs.python27Packages.callPackage ./nix/pydeps/natsort {};
    scikit-bio         = pkgs.python27Packages.callPackage ./nix/pydeps/scikit-bio {
      inherit CacheControl natsort;
    };
  };

  treeCl = myPython2.callPackage ./default.nix {
    inherit raxml; # TODO why doesn't it find this?
    inherit (myPython2) biopython;
    inherit (myPython2) fastcluster fasttree tree_distance progressbar-latest CacheControl scikit-bio phylo_utils;
    inherit (myPython2) pyyaml cython dendropy futures;
    inherit (myPython2) matplotlib nose numpy pandas progressbar scikitlearn scipy;
  };

in
  treeCl
