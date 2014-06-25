#!/bin/bash
./abundance_matrix.py  > abundance_matrix.out
./compare_annotations.py > compare_annotations.out
./download_metagenome_sequences.py MGR4440613.3 > download_metagenome_sequences.out
./dump_metagenome_metadata.py > dump_metagenome_metadata.out
./dump_project_metadata.py > dump_project_metadata.out
./dump_sequence_stats.py > dump_sequence_stats.out
./list_all_metagenomes.py > list_all_metagenomes.out
./list_all_projects.py > list_all_projects.out
./list_download_files.py > list_download_files.out
./sequences_with_annotations.py > sequences_with_annotations.out

