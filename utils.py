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
        None directly, instead uses command line args, requires all filled
        -p: platform : str
            Name of the trading platform the data is sourced from
        -i: input : str
            Filename of the file for the raw input transaction data
        -o: output : str
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

    def read_csv(self, in_or_out:str, invert:bool=False)->list:
        '''
        Reads the contents of either CSV file (input or output) into a 2D list

        Parameters
        ----------
        in_or_out : str
            Descriptor for which of the two files should be read
        invert : bool, optional
            Chooses whether the final output should be chronologically reversed

        Returns
        -------
        data : list
            2D list containing the data cells of the chosen CSV
        '''
        if in_or_out == "input":
            file = open(self.input)
        elif in_or_out == "output":
            file = open(self.output)
        else:
            print("Error: Invalid option for read_csv()")
            exit()
        data = [t.split(',') for t in file.read().split('\n')][1:-1]
        file.close()
        return (data if not invert else data[::-1])

    def write_csv(self):
        '''
        Opens a writable file variable for the output file

        Parameters
        ----------
        None

        Returns
        -------
        output_w : open(file)
            An opened, writable file variable of the output CSV
        '''
        output_w = open(self.output, "w")
        return output_w

    def type_compress(self, type:str)->str:
        '''
        Removes excess text from certain transaction type indicators

        Parameters
        ----------
        type : str
            A type indicator for a transaction

        Returns
        -------
        type : str
            The original type string, with uneccesary information removed
        '''
        if "->" in type:
            currs = type.split(" -> ")
            left, right = currs[0], currs[1]
            if left == "USD":
                return "Purchase"
            elif right == "USD":
                return "Sale"
            else:
                return "Sale"
        elif type == "Purchase":
            return "Purchase"
        elif type == "Crypto Earn":
            return "Earn Payment"
        elif type.split(" ")[0] == "Buy":
            return "Purchase"
        elif "Reward" in type and "Rewards" not in type or "Bonus" in type:
            return "Misc Taxable Reward"
        else:
            return "Unneeded"

    def format_tx(self, type:str, tx_i:int, date:str, amt:float, curr:str, usd_val:float, notes:str)->str:
        '''
        Takes in transaction data and creates the appropriate CSV output row

        Parameters
        ----------
        type : str
            Type indicator of the transaction
        tx_i : int
            Incrementing ID # of the transaction
        date : str
            Date the transaction took place
        amt : float
            Quantity of crypto transacted
        curr : str
            Name of currency or token transacted
        usd_val : float
            Value of the transaction in $
        notes : str
            Any provided notes about the transaction

        Returns
        -------
        tx : str
            Properly reformatted CSV row string for output file of form:
            Tx ID, Type, Type Helper, Date, Crypto Qty, Crypto Type, USD Val., Token Cost, Platform, Other Notes
        '''
        tx = self.platform[0:2] + str(tx_i) + "," + self.type_compress(type)
        tx += "," + "\"=B" + str(tx_i+1) + "&COUNTIF($B$2:B" + str(tx_i+1) + ",B" + str(tx_i+1) + ")\""
        tx += "," + date + "," + str(abs(amt)) + "," + curr + "," + str(abs(usd_val))
        tx += ",=G" + str(tx_i+1) + "/E" + str(tx_i+1) + "," + self.platform + "," + notes + "\n"
        return tx
