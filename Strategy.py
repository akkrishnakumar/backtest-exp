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
    
    def test_results(self):
        return [result.test_results for result in self.backtests]
    
    def run(self):
        
        print("\nInitiating Strategy...\n")        
        
        br()
        println("Creating Portfolio....")
        println("- Ranking stocks") 
        head = self.test_results()[0]
        p = Portfolio(self.rank(head)[:10])
        println("Portfolio Created !")
        
        println(f"PF init: {p.holdings}")

        br()
        println("Running Backtest...")
        for i, backtest in enumerate(self.backtests):
            
            target_date = backtest.target_date
            rebalanceUpdate = backtest.test_results
            ranked = self.rank(rebalanceUpdate)[:10]
            
            # if in holdings, don't replace
            # if not in holdings, then remove and calculate pnl of the trade
            # add to tradebook.
            
            rb_names = []
            for r in ranked:
               rb_names.append(r.name)
            rb_names = set(rb_names)
            
            pf_names = p.holding_names()
           
            newPf = []
            existing_entries = list(rb_names.intersection(pf_names))
            newPf.extend(existing_entries)
        
            # new_entries = list(rb_names.difference(pf_names))
            # newPf += new_entries
            
            print("\n")
            
            # println(f"rb_names: {rb_names}")
            # println(f"pf_names: {pf_names}")
            # println(f"Date: {target_date}")
            
            print(f"PF {i}: {newPf}")
            
            # How many ranked out ? Close positions
            toSell = list(pf_names.difference(rb_names))
            print(f"toSell {i}: {toSell}")
            p.close_positions(toSell, target_date)
            
            # Rebalancing the portfolio 
            p.update_holdings(ranked)
        
        # br()
        # for trade in p.tradebook:
        #     println(trade)
        #     println(trade.pnl_percent())
        #     br()
            
        return True