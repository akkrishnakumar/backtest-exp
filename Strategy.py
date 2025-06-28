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
        
        test_results = [result.test_results for result in self.backtests]
        head = test_results[0]
        tail = self.backtests[1:]
        
        br()
        println("Creating Portfolio....")
        println("- Ranking stocks") 
        p = Portfolio(self.rank(head)[:10])
        println("Portfolio Created !")
        
        println(f"PF init: {p.holdings}")

        br()
        println("Running Backtest...")
        for i, backtest in enumerate(tail):
            
            target_date = backtest.target_date
            rebalanceUpdate = backtest.test_results
            ranked = self.rank(rebalanceUpdate)[:10]     
            
            println(f"PF {i}:")
            p.rebalance(ranked, target_date)       
        
        br()
        pnl = 0
        for trade in p.tradebook:
            pnl += ((trade.sell_price / trade.buy_price) - 1) * 100

        println(f"PnL: {pnl}")
        return True