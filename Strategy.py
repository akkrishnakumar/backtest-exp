from Portfolio import Portfolio
from CLI import br, println

class Strategy_M_12_minus_1:
    
    def __init__(self, backtests):
        self.backtests = backtests
        
    # Sort a list of Ticker objects w.r.t. the gains 
    def rank(self, tickers):
        filteredTickers = [ticker for ticker in tickers if ticker.gain is not None]
        ranked_tickers = sorted(filteredTickers, key=lambda ticker: ticker.gain, reverse=True)
        return ranked_tickers
    
    def run(self):
        
        print("\nInitiating Strategy...\n")
        items = list(self.backtests.items())
        head = items[0]
        tail = items[1:] 
        
        for (i, h) in enumerate(head):
            println(f"{i} - {h}")
        
        br()
        println("Creating Portfolio....")
        println("- Ranking stocks") 
        p = Portfolio(self.rank(head[1])[:10])
        println("Portfolio Created !")
        
        br()
        println("Running Backtest...")
        for i, (target_date, rebalanceUpdate) in enumerate(tail):
            
            ranked = self.rank(rebalanceUpdate)[:10]
            
            # if in holdings, don't replace
            # if not in holdings, then remove and calculate pnl of the trade
            # add to tradebook.
            
            rb_names = []
            for r in ranked:
               rb_names.append(r.name)
            rb_names = set(rb_names)
            
            pf_names = set(p.holding_names())
           
            newPf = []
            existing_entries = list(rb_names.intersection(pf_names))
            newPf.extend(existing_entries)
        
            new_entries = list(rb_names.difference(pf_names))
            newPf += new_entries
            
            print("\n")
            
            println(f"rb_names: {rb_names}")
            println(f"pf_names: {pf_names}")
            println(f"Date: {target_date}")
            
            print(f"PF {i}: {newPf}")
            
            # How many ranked out ? Close positions
            toSell = list(pf_names.difference(rb_names))
            print(f"toSell {i}: {toSell}")
            # p.close_positions(toSell, target_date)
            
            # Rebalancing the portfolio 
            p.update_holdings(ranked)
        
        # br()
        # for trade in p.tradebook:
        #     println(trade)
        #     println(trade.pnl_percent())
        #     br()
            
        return True