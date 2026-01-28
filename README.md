# gene-sequence-data-pipeline
。

🐝 Honeybee Gene Sequence Analysis

A full-stack data pipeline for processing honeybee gene sequences using Python, Oracle, CGI, and machine learning.

## Overview

This project extracts gene sequences from raw biological data, computes nucleotide frequencies, stores results in an Oracle database, and performs K-Means clustering analysis. It integrates web input → database storage → data analysis → visualization.

## Features

- Web-based file upload via HTML + CGI

- Oracle database integration with batch insertion

- Dynamic database querying and web visualization

- K-Means clustering and 3D visualization (freq_A, freq_T, freq_GC)

## Structure
├── upload.html / confirm.html / result.html
├── upload.cgi / query.cgi
├── max_sequence_length.py
├── query_last_entry.py
├── kmeans_analysis.ipynb
├── honeybee_gene_sequences.txt
└── localCGIServer.py

## Usage

Start CGI server:

python localCGIServer.py


Open:

http://localhost:8081/upload.html


Upload data and view results.

Run K-Means analysis in Jupyter Notebook.
