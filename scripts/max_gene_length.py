# This program finds the maximum length of gene sequences

def main():

    infile = open("honeybee_gene_sequences.txt", "r")
    myStr = ""

    for line in infile:
        line = line.strip()

        # Same marker logic as in Data_Input_dynamic.cgi
        if ">gi" in line:
            line += "_**gene_seq_starts_here**_"

        myStr += line

    infile.close()

    entries = myStr.split(">gi|")

    max_len = 0

    for item in entries:
        if item.strip() == "":
            continue

        pos = item.find("_**gene_seq_starts_here**_")
        if pos == -1:
            continue

        seq = item[pos + len("_**gene_seq_starts_here**_") : ]

        # Keep only A,C,G,T
        seq = "".join([c for c in seq if c in "ACGT"])

        if len(seq) > max_len:
            max_len = len(seq)

    print("Maximum gene sequence length:", max_len)


if __name__ == "__main__":
    main()
