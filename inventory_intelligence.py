class InventoryIntelligence:
    """
    Module: Supply Chain Logic & Demand Forecasting
    Purpose: Automated Stock-Out Prediction for C-way Depot
    Lead: Irem Victor Chinonso (Director of Operations)
    """
    def calculate_runway(self, current_stock, velocity_history):
        """
        Calculates burn rate and predicts exhaustion date.
        """
        active_sales = [v for v in velocity_history if v > 0]
        if not active_sales:
            return {"avg_burn_rate": 0, "estimated_days_to_zero": float('inf')}
            
        avg_daily_sales = sum(active_sales) / len(active_sales)
        days_remaining = current_stock / avg_daily_sales if avg_daily_sales > 0 else float('inf')
        
        return {
            "avg_burn_rate": round(avg_daily_sales, 2),
            "estimated_days_to_zero": int(days_remaining) if days_remaining != float('inf') else "N/A"
        }
