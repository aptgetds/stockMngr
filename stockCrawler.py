import urllib
 
class Tick():
    def __init__(self):
        self.sym_list = []
        self.params = ""
 
    def add_stock(self, sym):
        if sym in set(self.sym_list):
            self.sym_list.remove(sym)
        self.sym_list.append(sym) 
 
    def remove_stock(self, sym):
        self.sym_list.remove(sym)
 
    def fetch(self): 
        str_sym_list = '+'.join(self.sym_list)
        str_param = self.params
        f = urllib.urlopen("http://finance.yahoo.com/d/quotes.csv?s=%s&f=%s" % (str_sym_list, str_param) ).read()
        rlt = f.split(",")
        return  rlt
