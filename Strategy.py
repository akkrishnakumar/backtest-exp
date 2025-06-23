from Portfolio import Portfolio

class Strategy_M_12_minus_1:
    
    # This can be a separate class
    # Will contain Initial captial, constituents etc
    portfolio = {} 
    

    def __init__(self, backtests):
        self.backtests = backtests
        
    # Sort a list of Ticker objects w.r.t. the gains 
    def rank(self, tickers):
        filteredTickers = [ticker for ticker in tickers if ticker.gain is not None]
        ranked_tickers = sorted(filteredTickers, key=lambda ticker: ticker.gain, reverse=True)
        return ranked_tickers
    
    def run(self):
        
        print("\nInitiating Strategy...\n")
        # print(self.backtests[0])
        start = self.backtests[0]
        
        print("\n Creating Portfolio....")
        print("\n - Ranking stocks") 
        p = Portfolio(self.rank(start)[:10])
        print("\n Portfolio Created....")
        
        print("\n Running Backtest...")
        tail = list(self.backtests.items())
        for i, rebalanceUpdate in tail[1:]:
            ranked = self.rank(rebalanceUpdate)[:10]
            
            rb_names = []
            for r in ranked:
               rb_names.append(r.name)
            rb_names = set(rb_names)
            # print(f"rb_names: {rb_names}")
            
            pf_names = p.holdings.keys()
            pf_names = set(pf_names)
            # print(f"pf_names: {pf_names}")
            
            newPf = []
            existing_entries = list(rb_names.intersection(pf_names))
            newPf.extend(existing_entries)
        
            new_entries = list(rb_names.difference(pf_names))
            newPf += new_entries
            
            print(f"PF {i}: {newPf}")
            
            # How many ranked out ? Close positions
            toSell = list(pf_names.difference(rb_names))
            print(f"toSell {i}: {toSell}")
            
            # How many still in top place ? 
            # How many new ? assign them the appropriate weights
            # rebalance portfolio
            
            p.holdings
            
        return True