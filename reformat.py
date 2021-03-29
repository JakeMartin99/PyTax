# Imports
from utils import Utils; ut = Utils()

# Get the 2D data list from the input file and a writable variable for the output file
input_data = ut.read_csv("input")
ref_file = ut.write_csv()

# Write the output file column headers and initialize the tx counter
ref_file.write("Tx ID,Type,Type Helper,Date,Crypto Qty,Crypto Type,USD Val.,Token Cost Basis,Platform,Other Notes\n")
tx_i = 1

# For each transaction in the input_data list...
for tx in input_data:
    # Retrieve all of the parameters from the transaction sub-list
    date = tx[0].split(' ')[0]
    type = tx[1]
    curr = tx[2]
    amt = float(tx[3])
    to_curr = tx[4]
    to_amt = float(tx[5]) if tx[5] else None
    native_curr = tx[6]
    usd_val = float(tx[7])
    usd_val2 = float(tx[8])
    tx_kind = tx[9]
    # Assert that the base currency is properly in USD and that relevant values match
    assert usd_val == usd_val2 and native_curr == "USD", "Error: Something wrong with USD data"
    # Fix MCO/CRO Overall Wallet Swap
    if type == "MCO/CRO Overall Wallet Swap":
        if curr == "MCO":
            type = "Sale"
        elif curr == "CRO":
            type = "Purchase"
    # Fix Dust Conversions
    if type == "Convert Dust":
        if curr != "CRO":
            type = "Sale"
        else:
            type = "Purchase"
    # Only add transaction if it is needed
    if ut.type_compress(type) != "Unneeded":
        # Create the reformatted transaction row CSV text and write it to the output file and
        new_tx = ut.format_tx(type, tx_i, date, amt, curr, usd_val, type)
        ref_file.write(new_tx)
        # Increment the tx counter
        tx_i += 1
        # If the transaction is a crypto -> crypto sale...
        if len(to_curr) > 0 and to_curr != "USD":
            # Add the crypto purchase corresponding to the above sale 
            new_tx2 = ut.format_tx("Purchase", tx_i, date, to_amt, to_curr, usd_val, "Combined with Above Sale")
            ref_file.write(new_tx2)
            # Increment the tx counter again
            tx_i += 1

# Close the output file
ref_file.close()

# Print list of output tx types
output_data = ut.read_csv("output")
tx_types = list(set([t[1] for t in output_data])); tx_types.sort()
[print(x) for x in tx_types]
