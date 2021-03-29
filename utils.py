# Imports
import sys

class Utils:
    '''
    A class to handle various utility features.
    ...
    Attributes
    ----------
    platform : str
        Name of the trading platform the data is sourced from
    input : str
        Filename of the file for the raw input transaction data
    output : str
        Filename of the destination file for the reformatted output transaction data

    Methods
    -------
    read_csv(in_or_out):
        Returns the contents of either input or output as a 2D list
    write_csv():
        Returns a writable IO variable for the output file
    type_compress():
        Removes excess text from certain transaction type indicators
    format_tx(type, tx_i, date, amt, curr, usd_val, notes):
        Takes in transaction data and creates the appropriate CSV output row
    '''
    
    def __init__(self):
        '''
        Constructs all necessary attributes for the utility object

        Parameters
        ----------
        None directly, instead uses command line args
        -p: platform: str
            Name of the trading platform the data is sourced from
        -i: input: str
            Filename of the file for the raw input transaction data
        -o: output: str
            Filename of the destination file for the reformatted output transaction data
        '''
        self.platform, self.input, self.output = "", "", ""
        args = sys.argv[1:]
        for i in range(len(args)):
            a = args[i]
            if a[0]=='-':
                flag = a[1]
                if flag == 'p':
                    if self.platform == "": self.platform = args[i+1]
                elif flag == 'i':
                    if self.input == "": self.input = args[i+1]
                elif flag == 'o':
                    if self.output == "": self.output = args[i+1]
                else:
                    print("Error: Unknown flag \'" + flag + "\' found")
                    exit()
        if self.platform=="" or self.input=="" or self.output=="":
            print("Error: Not all params filled")
            exit()

    def read_csv(self, in_or_out:str)->list:
        if in_or_out == "input":
            file = open(self.input)
        elif in_or_out == "output":
            file = open(self.output)
        else:
            print("Error: Invalid option for read_csv()")
            exit()
        data = [t.split(',') for t in file.read().split('\n')][1:-1][::-1]
        file.close()
        return data

    def write_csv(self):
        return open(self.output, "w")

    def type_compress(self, type:str)->str:
        if "->" in type:
            return ("Sale" if type.split(" -> ")[0] != "USD" else "Purchase")
        elif type == "Crypto Earn Deposit":
            return "Earn Deposit"
        elif type.split(" ")[-1] == "Deposit":
            return "Funds Transfer"
        else:
            return type

    def format_tx(self, type:str, tx_i:int, date:str, amt:float, curr:str, usd_val:float, notes:str)->str:
        tx = self.type_compress(type) + "," + "\"=A" + str(tx_i) + "&COUNTIF($A$2:A" + str(tx_i) + ",A" + str(tx_i) + ")\""
        tx += "," + date + "," + str(abs(amt)) + "," + curr + "," + str(abs(usd_val))
        tx += ",=F" + str(tx_i) + "/D" + str(tx_i) + "," + self.platform + "," + notes + "\n"
        return tx
