class Portfolio:
    
    holdings = {}
    
    def __init__(self, initialBuys):
        self.initialBuy = initialBuys
        print("\n Initializing Portfolio...")
        
        print("\n - Making first purchase")
        for initialBuy in initialBuys:
            self.holdings[initialBuy.name] = initialBuy

        print("\n Portfolio Initialized !")
    
    
        
        