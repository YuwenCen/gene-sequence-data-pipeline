import oracledb as cx_Oracle


def main():

    # connect to Oracle
    con = cx_Oracle.connect("yuwen/12345@10.0.2.15:1521/xe")
    cur = con.cursor()

    target_gi = '147907436'

    cur.execute(
        '''
        select sequence from beeGenes
        where gi = :gi
        ''',
        gi=target_gi
    )

    row = cur.fetchone()

    gene_seq = row[0]
    print("Gene sequence for gi =", target_gi)
    print(gene_seq)

    cur.close()
    con.close()


if __name__ == "__main__":
    main()
