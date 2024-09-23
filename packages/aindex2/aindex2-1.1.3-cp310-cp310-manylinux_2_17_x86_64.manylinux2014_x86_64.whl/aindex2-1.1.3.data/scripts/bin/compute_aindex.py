#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# @created: 01.01.2017
# @author: Aleksey Komissarov
# @contact: ad3002@gmail.com

import argparse
import os
import subprocess

def runner(commands):
    for command in commands:
        print(command)
        subprocess.run(command, shell=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compute index.")
    parser.add_argument(
        "-i", help="Fasta, comma separated fastqs or reads", required=True
    )
    parser.add_argument(
        "-j", help="JF2 file if exists [None]", required=False, default=None
    )
    parser.add_argument(
        "--index", help="Index prefix if exists [None]", required=False, default=None
    )
    parser.add_argument(
        "-t",
        help="Reads type reads, fasta, fastq, se [fastq]",
        required=False,
        default="fastq",
    )
    parser.add_argument("-o", help="Output prefix", required=True)
    parser.add_argument("--lu", help="-L for jellyfish [0]", required=False, default=0)
    parser.add_argument("--up", help="-U for jellyfish [1000000000]", required=False, default=1000000000)
    parser.add_argument("--sort", help="Sort dat file [None]", required=False, default=None)
    parser.add_argument(
        "--interactive", help="Interactive [None]", required=False, default=None
    )
    parser.add_argument("-P", help="Threads [12]", required=False, default=12)
    parser.add_argument("-M", help="JF2 memory in Gb [5]", required=False, default=5)
    parser.add_argument(
        "--onlyindex", help="Compute only index [False]", required=False, default=False
    )
    parser.add_argument(
        "--unzip", help="Unzip files [False]", required=False, default=False
    )
    parser.add_argument(
        "--kmers", help="Make kmers file [False]", required=False, default=False
    )
    parser.add_argument(
        "--path_to_aindex",
        help="Path to aindex folder including / ['']",
        required=False,
        default=None,
    )

    args = vars(parser.parse_args())

    reads_file = args["i"]
    prefix = args["o"]
    reads_type = args["t"]
    threads = args["P"]
    jf2_file = args["j"]
    sort_dat_file = args["sort"]
    unzip = args["unzip"]
    memory = args["M"]
    interactive = args["interactive"]
    only_index = args["onlyindex"]
    index_prefix = args["index"]
    path_to_aindex = args["path_to_aindex"]

    if path_to_aindex is None:
        path_to_aindex = ""

    # Check if input required files exist
    required_files = reads_file.split(",")
    missing_files = [
        file for file in required_files if file and not os.path.exists(file)
    ]

    if missing_files:
        print("The following files are missing:")
        for file in missing_files:
            print(file)
        exit(1)

    make_kmers = bool(args["kmers"])

    lu = args["lu"]
    up = args["up"]

    if unzip:
        local_files = reads_file.split(",")
        for file_name in local_files:
            command = "gzip -d %s" % file_name
            runner(command)

    if not jf2_file and not index_prefix:
        # TODO: fix reads renaming if -t reads and different prefix
        if reads_type == "reads":
            commands = [
                f"{path_to_aindex}reads_to_fasta.py -i {reads_file} -o {prefix}.fa",
                f"jellyfish count -m 23 -t {threads} -s {memory}G -C -L {lu} -U {up} -o {prefix}.23.jf2 {prefix}.fa",
            ]
            runner(commands)
            
            if interactive:
                input("Continue?")
        elif reads_type == "fasta" or reads_type == "fastq" or reads_type == "se":
            commands = [
                f"jellyfish count -m 23 -t %s -s %sG -C -L %s -U %s -o %s.23.jf2 %s"
                % (threads, memory, lu, up, prefix, reads_file.replace(",", " ")),
            ]
            runner(commands)
            if interactive:
                input("Continue?")

        jf2_file = "%s.23.jf2" % prefix

        ### here we expect that jf2 file is created
        if not os.path.exists(jf2_file):
            print("JF2 file is missing, please, check jellyfish command")
            exit(1)

    commands = []

    if not only_index:
        
        if reads_type == "fasta":
            commands = [
                f"{path_to_aindex}compute_reads.exe {reads_file} - fasta {prefix}",
            ]
        if reads_type == "fastq":
            commands = [
                f"{path_to_aindex}compute_reads.exe {reads_file.replace(',', ' ')} fastq {prefix}",
            ]
        if reads_type == "se":
            commands = [
                f"{path_to_aindex}compute_reads.exe {reads_file.replace(',', ' ')} - se {prefix}",
            ]

        runner(commands)

        ### here we expect that reads file is created
        if not os.path.exists("%s.reads" % prefix):
            print("Reads file is missing, please, check conversion command")
            exit(1)

    if not index_prefix:
        if lu:
            commands = [
                f"jellyfish dump -t -c -L {lu} -o {prefix}.23.dat {jf2_file}",
            ]
        else:
            commands = [
                f"jellyfish dump -t -c -o {prefix}.23.dat {jf2_file}",
            ]

        runner(commands)

        if sort_dat_file:
            commands = [
                f"sort -k2nr {prefix}.23.dat > {prefix}.23.sdat",
            ]
            runner(commands)

        commands = [
            f"jellyfish histo -o {prefix}.23.histo {jf2_file}",
            f"cut -f1 {prefix}.23.dat > {prefix}.23.kmers",
            f"{path_to_aindex}compute_mphf_seq {prefix}.23.kmers {prefix}.23.pf",
            f"{path_to_aindex}compute_index.exe {prefix}.23.dat {prefix}.23.pf {prefix}.23 {threads} 0",
        ]
        runner(commands)

    if not only_index:
        commands = [
            f"{path_to_aindex}compute_aindex.exe {prefix}.reads {prefix}.23.pf {prefix}.23 {prefix}.23 {threads} 23 {prefix}.23.tf.bin",
        ]
        runner(commands)

    if make_kmers:
        commands = [
            f"rm {prefix}.23.dat {prefix}.23.jf2",
        ]
    else:
        commands = [
            f"rm {prefix}.23.dat {prefix}.23.kmers {prefix}.23.jf2",
        ]

    runner(commands)
