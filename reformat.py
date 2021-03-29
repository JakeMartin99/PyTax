import sys
from utils import Utils; ut = Utils()
args = sys.argv[1:]
ut.handle_args(args)

input_data = ut.read_csv("input")
ref_file = ut.write_csv()
ref_file.write("Type,Type Helper,Date,Crypto Qty,Crypto Type,USD Val.,Token Cost Basis,Platform,Other Notes\n")
tx_i = 2
for tx in input_data:
    date = tx[0].split(' ')[0]
    type = tx[1]
    curr = tx[2]
    amt = float(tx[3])
    to_curr = tx[4]
    to_amt = float(tx[5]) if tx[5] else None
    native_curr = tx[6]
    usd_val = float(tx[7])
    usd_val2 = float(tx[8])
    new_tx = ut.format_tx(type, tx_i, date, amt, curr, usd_val, type)
    if usd_val != usd_val2 or native_curr != "USD":
        print("Error: Something wrong with USD data")
        exit()
    ref_file.write(new_tx)
    tx_i += 1
    if len(to_curr) > 0:
        new_tx2 = ut.format_tx("Purchase", tx_i, date, to_amt, to_curr, usd_val, "Combined with Above")
        ref_file.write(new_tx2)
        tx_i += 1
ref_file.close()

output_data = ut.read_csv("output")
tx_types = list(set([t[0] for t in output_data])); tx_types.sort()
[print(x) for x in tx_types]
