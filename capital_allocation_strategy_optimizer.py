"""
Statistical Business Architect Toolkit: Capital Allocation Optimizer
Vibe: The Director | Logic: Reinvestment vs Liquidity

Where the capital flows, the empire grows. This script optimizes the split 
between R&D, Marketing, and Treasury.
"""

def optimize_allocation(free_cash_flow, growth_targets):
    """
    Allocates capital to maximize ROI based on historical performance.
    """
    print("Architecting Capital Flow...")
    
    # Weighted allocation based on target priority
    total_priority = sum(growth_targets.values())
    allocation = {}
    
    for sector, priority in growth_targets.items():
        share = priority / total_priority
        amount = free_cash_flow * share
        allocation[sector] = round(amount, 2)
        
    return allocation

if __name__ == "__main__":
    targets = {"R&D": 5, "Marketing": 8, "Treasury": 3}
    cash = 500000 # Monthly Surplus
    
    plan = optimize_allocation(cash, targets)
    print(f"Strategic Allocation: {plan}")
