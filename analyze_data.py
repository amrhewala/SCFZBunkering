#!/usr/bin/env python3
"""
تحليل البيانات والتصور - دراسة تموين السفن
Data Analysis and Visualization - Ship Supply Study

This script analyzes the statistical data from the Suez Canal ship supply sector
and generates insights and visualizations.
"""

import csv
import json
from datetime import datetime
from pathlib import Path


def read_csv(filename):
    """Read CSV file and return data as list of dictionaries"""
    data = []
    filepath = Path(__file__).parent / 'data' / filename
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            data = list(reader)
        print(f"✓ Successfully loaded {filename}: {len(data)} records")
    except FileNotFoundError:
        print(f"✗ File not found: {filename}")
    except Exception as e:
        print(f"✗ Error reading {filename}: {str(e)}")
    
    return data


def analyze_statistical_data(data):
    """Analyze historical and projected statistical data"""
    print("\n" + "="*70)
    print("تحليل البيانات الإحصائية - Statistical Data Analysis")
    print("="*70)
    
    if not data:
        print("No data available for analysis")
        return
    
    # Calculate growth metrics
    years = [int(row['Year']) for row in data]
    revenues = [float(row['Market_Size_Million_USD']) for row in data]
    ships = [int(row['Total_Ships']) for row in data]
    
    # Historical period (2019-2024)
    historical_years = [y for y in years if y <= 2024]
    historical_revenues = revenues[:len(historical_years)]
    
    # Projected period (2025-2030)
    projected_years = [y for y in years if y > 2024]
    projected_revenues = revenues[len(historical_years):]
    
    # Calculate CAGR for historical period
    if len(historical_revenues) > 1:
        start_revenue = historical_revenues[0]
        end_revenue = historical_revenues[-1]
        years_count = len(historical_revenues) - 1
        cagr_historical = ((end_revenue / start_revenue) ** (1/years_count) - 1) * 100
        
        print(f"\n📊 Historical Period (2019-2024):")
        print(f"   Starting Revenue: ${start_revenue}M")
        print(f"   Ending Revenue: ${end_revenue}M")
        print(f"   CAGR: {cagr_historical:.2f}%")
    
    # Calculate CAGR for projected period
    if len(projected_revenues) > 1:
        start_revenue = historical_revenues[-1]
        end_revenue = projected_revenues[-1]
        years_count = len(projected_years)
        cagr_projected = ((end_revenue / start_revenue) ** (1/years_count) - 1) * 100
        
        print(f"\n📈 Projected Period (2025-2030):")
        print(f"   Starting Revenue: ${start_revenue}M")
        print(f"   Target Revenue: ${end_revenue}M")
        print(f"   Target CAGR: {cagr_projected:.2f}%")
        print(f"   Total Growth: {((end_revenue/start_revenue - 1) * 100):.1f}%")
    
    # Display year-by-year data
    print(f"\n📋 Year-by-Year Breakdown:")
    print(f"{'Year':<6} {'Ships':>10} {'Revenue ($M)':>15} {'Growth %':>12} {'Employment':>12}")
    print("-" * 70)
    
    for row in data:
        year = row['Year']
        ships = row['Total_Ships']
        revenue = row['Market_Size_Million_USD']
        growth = row['Growth_Rate_Percent']
        employment = row['Direct_Employment']
        
        growth_indicator = "▲" if float(growth) > 0 else "▼"
        print(f"{year:<6} {ships:>10} {revenue:>15} {growth_indicator}{growth:>10} {employment:>12}")


def analyze_service_breakdown(data):
    """Analyze service category distribution"""
    print("\n" + "="*70)
    print("تحليل توزيع الخدمات - Service Distribution Analysis")
    print("="*70)
    
    if not data:
        print("No data available for analysis")
        return
    
    total_revenue = sum(float(row['Revenue_2024_Million_USD']) for row in data)
    
    print(f"\n💰 Total Service Revenue (2024): ${total_revenue:.1f}M")
    print(f"\n{'Service Category':<25} {'%':>8} {'Revenue ($M)':>15} {'Potential':>15}")
    print("-" * 70)
    
    for row in sorted(data, key=lambda x: float(x['Percentage']), reverse=True):
        category = row['Service_Category'].replace('_', ' ')
        percentage = row['Percentage']
        revenue = float(row['Revenue_2024_Million_USD'])
        potential = row['Growth_Potential']
        
        # Visual bar
        bar_length = int(float(percentage) / 5)
        bar = "█" * bar_length
        
        print(f"{category:<25} {percentage:>7}% {revenue:>14.1f} {potential:>15}")
        print(f"  {bar}")


def analyze_ship_types(data):
    """Analyze ship type distribution"""
    print("\n" + "="*70)
    print("تحليل أنواع السفن - Ship Type Analysis")
    print("="*70)
    
    if not data:
        print("No data available for analysis")
        return
    
    total_ships = sum(int(row['Annual_Count_2024']) for row in data)
    total_value = sum(int(row['Annual_Count_2024']) * int(row['Average_Supply_Value_USD']) 
                     for row in data)
    
    print(f"\n🚢 Total Ships Served (2024): {total_ships:,}")
    print(f"💵 Total Supply Value (2024): ${total_value/1_000_000:.1f}M")
    
    print(f"\n{'Ship Type':<25} {'%':>8} {'Count':>12} {'Avg Value ($)':>15} {'Total ($M)':>15}")
    print("-" * 80)
    
    for row in sorted(data, key=lambda x: float(x['Percentage']), reverse=True):
        ship_type = row['Ship_Type'].replace('_', ' ')
        percentage = row['Percentage']
        count = int(row['Annual_Count_2024'])
        avg_value = int(row['Average_Supply_Value_USD'])
        total = count * avg_value / 1_000_000
        
        print(f"{ship_type:<25} {percentage:>7}% {count:>12,} ${avg_value:>14,} ${total:>14.1f}")


def analyze_geographic_distribution(data):
    """Analyze geographic client distribution"""
    print("\n" + "="*70)
    print("التوزيع الجغرافي للعملاء - Geographic Client Distribution")
    print("="*70)
    
    if not data:
        print("No data available for analysis")
        return
    
    print(f"\n{'Region':<20} {'Client %':>12} {'Revenue %':>15} {'Alignment':>15}")
    print("-" * 70)
    
    for row in sorted(data, key=lambda x: float(x['Client_Percentage']), reverse=True):
        region = row['Region']
        client_pct = float(row['Client_Percentage'])
        revenue_pct = float(row['Revenue_Contribution_Percent'])
        
        # Check alignment between client % and revenue %
        alignment = revenue_pct / client_pct if client_pct > 0 else 0
        alignment_text = "High Value" if alignment > 1.1 else "Aligned" if alignment > 0.9 else "Low Value"
        
        print(f"{region:<20} {client_pct:>11}% {revenue_pct:>14}% {alignment_text:>15}")


def analyze_financial_projections(data):
    """Analyze financial projections"""
    print("\n" + "="*70)
    print("التوقعات المالية - Financial Projections")
    print("="*70)
    
    if not data:
        print("No data available for analysis")
        return
    
    print(f"\n{'Year':<6} {'Revenue':>12} {'Net Profit':>15} {'Net Margin':>15} {'Growth':>12}")
    print("-" * 70)
    
    prev_revenue = None
    for row in data:
        year = row['Year']
        revenue = float(row['Revenue_Million_USD'])
        net_profit = float(row['Net_Profit_Million_USD'])
        net_margin = float(row['Net_Margin_Percent'])
        
        if prev_revenue:
            growth = ((revenue / prev_revenue) - 1) * 100
            growth_text = f"+{growth:.1f}%"
        else:
            growth_text = "-"
        
        print(f"{year:<6} ${revenue:>10.0f}M ${net_profit:>13.0f}M {net_margin:>14.1f}% {growth_text:>12}")
        prev_revenue = revenue
    
    # Calculate cumulative profits
    total_profit = sum(float(row['Net_Profit_Million_USD']) for row in data)
    print(f"\n💰 Cumulative Net Profit (2025-2030): ${total_profit:.0f}M")


def analyze_kpis(data):
    """Analyze Key Performance Indicators"""
    print("\n" + "="*70)
    print("مؤشرات الأداء الرئيسية - Key Performance Indicators (KPIs)")
    print("="*70)
    
    if not data:
        print("No data available for analysis")
        return
    
    # Group by category
    categories = {}
    for row in data:
        category = row['KPI_Category']
        if category not in categories:
            categories[category] = []
        categories[category].append(row)
    
    for category, kpis in categories.items():
        print(f"\n📊 {category} KPIs:")
        print(f"{'Metric':<30} {'2024':>12} {'2027':>12} {'2030':>12} {'Improvement':>15}")
        print("-" * 85)
        
        for kpi in kpis:
            metric = kpi['Metric'].replace('_', ' ')
            current = kpi['Current_2024']
            target_2027 = kpi['Target_2027']
            target_2030 = kpi['Target_2030']
            unit = kpi['Unit'].replace('_', ' ')
            
            # Calculate improvement
            try:
                current_val = float(current.replace(',', ''))
                target_val = float(target_2030.replace(',', ''))
                improvement = ((target_val / current_val - 1) * 100)
                improvement_text = f"+{improvement:.1f}%"
            except (ValueError, TypeError, ZeroDivisionError):
                improvement_text = "-"
            
            # Format values with units
            current_str = f"{current} {unit}"
            target_2027_str = f"{target_2027} {unit}"
            target_2030_str = f"{target_2030} {unit}"
            
            print(f"{metric:<30} {current_str:>12} {target_2027_str:>12} {target_2030_str:>12} {improvement_text:>15}")


def generate_summary_report():
    """Generate comprehensive summary report"""
    print("\n" + "="*70)
    print("التقرير الملخص - Summary Report")
    print("="*70)
    print(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    print("\n🎯 Strategic Highlights:")
    print("   • Market Opportunity: $1.5B by 2030")
    print("   • Investment Required: $60M over 3 years")
    print("   • Expected IRR: 28.5%")
    print("   • Payback Period: 4.2 years")
    print("   • Target Market Share: 85% by 2030")
    print("   • Jobs Created: 2,390 new positions by 2030")
    
    print("\n✅ Key Success Factors:")
    print("   1. Digital transformation (100% by 2027)")
    print("   2. Strategic partnerships (30 by 2030)")
    print("   3. Human capital development (5,000 trained)")
    print("   4. Environmental sustainability (carbon neutral)")
    print("   5. Service excellence (95% customer satisfaction)")
    
    print("\n📈 Growth Trajectory:")
    print("   • 2025: Foundation & Preparation")
    print("   • 2026-2027: Expansion & Growth")
    print("   • 2028-2030: Leadership & Innovation")


def main():
    """Main analysis function"""
    print("\n" + "="*70)
    print("🚢 Suez Canal Ship Supply Sector - Data Analysis")
    print("   تحليل بيانات قطاع تموين السفن - قناة السويس")
    print("="*70)
    
    # Load all data files
    statistical_data = read_csv('statistical_analysis.csv')
    service_data = read_csv('service_breakdown.csv')
    ship_types_data = read_csv('ship_types_distribution.csv')
    geographic_data = read_csv('geographic_distribution.csv')
    financial_data = read_csv('financial_projections.csv')
    kpi_data = read_csv('kpis.csv')
    
    # Run analyses
    if statistical_data:
        analyze_statistical_data(statistical_data)
    
    if service_data:
        analyze_service_breakdown(service_data)
    
    if ship_types_data:
        analyze_ship_types(ship_types_data)
    
    if geographic_data:
        analyze_geographic_distribution(geographic_data)
    
    if financial_data:
        analyze_financial_projections(financial_data)
    
    if kpi_data:
        analyze_kpis(kpi_data)
    
    # Generate summary
    generate_summary_report()
    
    print("\n" + "="*70)
    print("✓ Analysis Complete")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
