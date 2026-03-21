# Project Structure

This file is a quick map of the public repository. Use [README.md](README.md) for build and run instructions.

## Directory Layout

```text
jn_cuclark/
├── README.md
├── LICENSE
├── STRUCTURE.md
├── install.sh
├── .gitignore
├── app/
│   ├── Makefile
│   ├── kent.cpp
│   └── kent_mpi.cpp
├── config/
│   └── cluster.conf.example
├── logs/
│   └── .gitkeep
├── results/
│   └── .gitkeep
├── scripts/
│   ├── classify_metagenome.sh
│   ├── clean.sh
│   ├── estimate_abundance.sh
│   ├── make_metadata.sh
│   ├── set_targets.sh
│   ├── updateTaxonomy.sh
│   └── download/
│       ├── download_data.sh
│       ├── download_data_newest.sh
│       ├── download_data_release.sh
│       └── download_taxondata.sh
└── src/
    ├── Makefile
    ├── CuClarkDB.cu
    ├── CuClarkDB.cuh
    ├── CuCLARK_hh.hh
    ├── HashTableStorage_hh.hh
    ├── analyser.cc
    ├── analyser.hh
    ├── dataType.hh
    ├── file.cc
    ├── file.hh
    ├── getAbundance.cc
    ├── getAccssnTaxID.cc
    ├── getTargetsDef.cc
    ├── getfilesToTaxNodes.cc
    ├── hashTable_hh.hh
    ├── kmersConversion.cc
    ├── kmersConversion.hh
    ├── main.cc
    ├── parameters.hh
    └── parameters_light_hh
```

## What Lives Where

- `app/`: front-end programs and the top-level build targets used by this repository
- `src/`: CUDA/C++ implementation of `cuCLARK`, `cuCLARK-l`, and helper binaries
- `scripts/`: shell wrappers for database preparation, classification, abundance estimation, cleanup, and data/taxonomy downloads
- `config/cluster.conf.example`: template for MPI runs; local `config/cluster.conf` files are intentionally not tracked
- `logs/` and `results/`: generated outputs; these directories are kept in the repo with `.gitkeep`

## Generated Local State

The following are created during local use and are not part of the public source tree:

- `bin/`: compiled executables
- `config/cluster.conf`: local MPI configuration copied from the example
- `scripts/.settings`, `.DBDirectory`, `.taxondata`, `files_excluded.txt`: local database metadata
- database contents and input reads
