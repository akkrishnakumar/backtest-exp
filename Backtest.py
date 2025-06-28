class Backtest:
    
    def __init__(self, target_date, test_results):
        self.target_date = target_date
        self.test_results = test_results
    
    def __str__(self):
        return f"Backtest(Target Date: {self.target_date}, Test Result: {self.test_results})"
    
    def __repr__(self):
        return str(self)