import matplotlib
matplotlib.use('Agg') # Use non-interactive backend to prevent GUI threads issues

import matplotlib.pyplot as plt
import database
import asyncio
from typing import Optional

class CRMAnalytics:
    """
    Queries database and generates statistics charts.
    """
    
    @staticmethod
    async def generate_report_image() -> Optional[str]:
        """
        Creates a dual line-bar chart for users and revenue.
        Saves it as crm_analytics.png and returns the path.
        """
        user_stats, sales_stats = await database.get_analytics_data()
        
        if not user_stats:
            return None
            
        # Parse datasets
        user_dates = [row[0] for row in user_stats]
        user_counts = [row[1] for row in user_stats]
        
        sales_dates = [row[0] for row in sales_stats]
        sales_revenue = [row[1] for row in sales_stats]
        
        # Merge dates to keep a aligned x-axis
        all_dates = sorted(list(set(user_dates + sales_dates)))
        
        # Map values
        reg_map = {d: 0 for d in all_dates}
        rev_map = {d: 0.0 for d in all_dates}
        
        for d, count in user_stats:
            reg_map[d] = count
        for d, rev in sales_stats:
            rev_map[d] = rev
            
        dates_formatted = [d[5:] for d in all_dates] # MM-DD
        registrations = [reg_map[d] for d in all_dates]
        revenue = [rev_map[d] for d in all_dates]

        # Heavy Matplotlib rendering wrapped in an executor thread
        def _render():
            plt.style.use('dark_background')
            
            fig, ax1 = plt.subplots(figsize=(10, 5))
            
            # Line chart for user registrations on left y-axis
            color_blue = '#3b82f6'
            ax1.set_xlabel('Дата', fontsize=12, labelpad=10)
            ax1.set_ylabel('Новые клиенты', color=color_blue, fontsize=12)
            line = ax1.plot(dates_formatted, registrations, color=color_blue, marker='o', linewidth=2.5, label='Регистрации')
            ax1.tick_params(axis='y', labelcolor=color_blue)
            ax1.grid(True, alpha=0.1)
            
            # Bar chart for revenue on right y-axis
            ax2 = ax1.twinx()
            color_green = '#10b981'
            ax2.set_ylabel('Выручка (руб.)', color=color_green, fontsize=12)
            bars = ax2.bar(dates_formatted, revenue, color=color_green, alpha=0.3, width=0.4, label='Выручка')
            ax2.tick_params(axis='y', labelcolor=color_green)
            
            plt.title('Аналитика продаж и регистраций (7 дней) // Nexus CRM', fontsize=14, pad=15, fontweight='bold')
            
            fig.tight_layout()
            
            output_file = "crm_analytics.png"
            plt.savefig(output_file, dpi=200)
            plt.close()
            return output_file

        return await asyncio.to_thread(_render)
