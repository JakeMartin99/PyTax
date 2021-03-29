class Utils:
    '''
    Initialize the Utils class with empty parameters for
    -platform: Identifies the trading platform data is sourced from
    -input: Filename for the input transaction data
    -output: Filename for the reformatted output data
    '''
    def __init__(self):
        self.platform, self.input, self.output = "", "", ""

    '''
    '''
    def handle_args(self, args:list):
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
