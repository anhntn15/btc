import csv
import json


def json_to_csv(inp_path: str, out_path: str, *args):
    """
    convert raw data in json format to csv format
    :param inp_path:
    :param out_path:
    :param args: if specified, the column of csv file will be ordered like that
    """
    fin = open(inp_path, 'r')
    if len(args) > 0:
        headers = list(args)
    else:
        record = json.loads(fin.readline())  # get one record
        headers = list(record.keys())
        fin.seek(0)  # read from beginning

    fout = open(out_path, 'w', newline='')
    writer = csv.DictWriter(fout, headers, extrasaction='ignore')
    writer.writeheader()

    for line in fin.readlines():
        try:
            record = json.loads(line)
            writer.writerow(dict(record))
        except Exception as e:
            print('Error', e)

    fin.close()
    fout.close()
    print(f'created {out_path}')
