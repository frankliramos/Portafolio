"""
Customer Risk Segmentation Analysis for Telco
==============================================

This script implements a comprehensive customer segmentation strategy based on risk assessment.
It categorizes customers into different risk segments for targeted marketing, risk management, 
and service customization.

Author: Portfolio Project
Date: 2024
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

class CustomerRiskSegmentation:
    """
    A comprehensive customer risk segmentation system that analyzes multiple risk factors
    to categorize customers into actionable risk segments.
    """
    
    def __init__(self, data_path):
        """Initialize the segmentation system with customer data."""
        self.data_path = data_path
        self.df = None
        self.risk_scores = None
        self.segments = None
        self.scaler = StandardScaler()
        
    def load_and_prepare_data(self):
        """Load and prepare the customer data for analysis."""
        print("Loading customer data...")
        self.df = pd.read_csv(self.data_path)
        
        # Convert TotalCharges to numeric (handle any string values)
        self.df['TotalCharges'] = pd.to_numeric(self.df['TotalCharges'], errors='coerce')
        self.df['TotalCharges'].fillna(0, inplace=True)
        
        print(f"Loaded {len(self.df)} customer records with {len(self.df.columns)} features")
        return self.df
    
    def calculate_churn_risk_score(self):
        """Calculate churn risk score using multiple factors."""
        # Tenure-based risk (lower tenure = higher risk)
        tenure_risk = (self.df['tenure'].max() - self.df['tenure']) / self.df['tenure'].max()
        
        # Contract-based risk
        contract_risk = self.df['Contract'].map({
            'Month-to-month': 1.0,
            'One year': 0.5,
            'Two year': 0.2
        })
        
        # Payment method risk
        payment_risk = self.df['PaymentMethod'].map({
            'Electronic check': 1.0,
            'Mailed check': 0.7,
            'Bank transfer (automatic)': 0.3,
            'Credit card (automatic)': 0.2
        })
        
        # Service complexity risk (more services = potentially higher satisfaction but also complexity)
        service_features = ['PhoneService', 'InternetService', 'OnlineSecurity', 'OnlineBackup',
                           'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies']
        service_count = 0
        for service in service_features:
            if service in self.df.columns:
                service_count += (self.df[service] != 'No').astype(int)
        
        service_complexity_risk = np.clip(service_count / len(service_features), 0, 1)
        
        # Combine risk factors
        churn_risk = (tenure_risk * 0.3 + contract_risk * 0.3 + payment_risk * 0.25 + 
                     service_complexity_risk * 0.15)
        
        return churn_risk
    
    def calculate_revenue_risk_score(self):
        """Calculate revenue risk based on charges and payment patterns."""
        # Monthly charges risk (very low or very high charges can be risky)
        monthly_charges_norm = self.df['MonthlyCharges'] / self.df['MonthlyCharges'].max()
        
        # Revenue volatility risk (ratio of monthly to average expected total)
        expected_total = self.df['MonthlyCharges'] * self.df['tenure']
        actual_total = self.df['TotalCharges']
        
        # Handle division by zero
        revenue_volatility = np.where(expected_total > 0, 
                                    np.abs(actual_total - expected_total) / expected_total, 
                                    0)
        revenue_volatility = np.clip(revenue_volatility, 0, 2)
        
        # Senior citizen additional risk
        senior_risk = self.df['SeniorCitizen'] * 0.2
        
        # Combine revenue risk factors
        revenue_risk = monthly_charges_norm * 0.4 + revenue_volatility * 0.4 + senior_risk * 0.2
        
        return revenue_risk
    
    def calculate_overall_risk_score(self):
        """Calculate comprehensive risk score combining multiple dimensions."""
        print("Calculating risk scores...")
        
        # Calculate individual risk components
        churn_risk = self.calculate_churn_risk_score()
        revenue_risk = self.calculate_revenue_risk_score()
        
        # Use actual churn data if available for validation
        if 'Churn' in self.df.columns:
            churn_actual = (self.df['Churn'] == 'Yes').astype(float)
            # Weight actual churn behavior heavily if we have it
            overall_risk = (churn_risk * 0.3 + revenue_risk * 0.3 + churn_actual * 0.4)
        else:
            overall_risk = (churn_risk * 0.6 + revenue_risk * 0.4)
        
        # Normalize to 0-100 scale
        self.risk_scores = (overall_risk * 100).round(2)
        self.df['RiskScore'] = self.risk_scores
        
        return self.risk_scores
    
    def create_risk_segments(self):
        """Create risk segments based on risk scores."""
        print("Creating risk segments...")
        
        # Define risk thresholds
        def categorize_risk(score):
            if score >= 75:
                return 'Critical Risk'
            elif score >= 50:
                return 'High Risk'
            elif score >= 25:
                return 'Medium Risk'
            else:
                return 'Low Risk'
        
        self.df['RiskSegment'] = self.df['RiskScore'].apply(categorize_risk)
        self.segments = self.df['RiskSegment'].value_counts()
        
        print("Risk Segment Distribution:")
        print(self.segments)
        print(f"\nSegment Percentages:")
        print((self.segments / len(self.df) * 100).round(1))
        
        return self.segments
    
    def analyze_segments(self):
        """Analyze characteristics of each risk segment."""
        print("\n" + "="*60)
        print("RISK SEGMENT ANALYSIS")
        print("="*60)
        
        segment_analysis = {}
        
        for segment in self.df['RiskSegment'].unique():
            segment_data = self.df[self.df['RiskSegment'] == segment]
            
            analysis = {
                'count': len(segment_data),
                'percentage': len(segment_data) / len(self.df) * 100,
                'avg_tenure': segment_data['tenure'].mean(),
                'avg_monthly_charges': segment_data['MonthlyCharges'].mean(),
                'avg_total_charges': segment_data['TotalCharges'].mean(),
                'churn_rate': (segment_data['Churn'] == 'Yes').mean() * 100 if 'Churn' in segment_data.columns else 0,
                'senior_citizen_rate': segment_data['SeniorCitizen'].mean() * 100,
                'contract_types': segment_data['Contract'].value_counts(normalize=True).to_dict(),
                'payment_methods': segment_data['PaymentMethod'].value_counts(normalize=True).to_dict()
            }
            
            segment_analysis[segment] = analysis
            
            print(f"\n{segment.upper()}:")
            print(f"  Customer Count: {analysis['count']} ({analysis['percentage']:.1f}%)")
            print(f"  Average Tenure: {analysis['avg_tenure']:.1f} months")
            print(f"  Average Monthly Charges: ${analysis['avg_monthly_charges']:.2f}")
            print(f"  Average Total Charges: ${analysis['avg_total_charges']:.2f}")
            if 'Churn' in self.df.columns:
                print(f"  Churn Rate: {analysis['churn_rate']:.1f}%")
            print(f"  Senior Citizens: {analysis['senior_citizen_rate']:.1f}%")
            
            # Top contract type
            top_contract = max(analysis['contract_types'].items(), key=lambda x: x[1])
            print(f"  Most Common Contract: {top_contract[0]} ({top_contract[1]*100:.1f}%)")
            
            # Top payment method
            top_payment = max(analysis['payment_methods'].items(), key=lambda x: x[1])
            print(f"  Most Common Payment: {top_payment[0]} ({top_payment[1]*100:.1f}%)")
        
        return segment_analysis
    
    def generate_visualizations(self):
        """Generate comprehensive visualizations of risk segmentation."""
        print("\nGenerating visualizations...")
        
        # Set up the plotting style
        plt.style.use('default')
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('Customer Risk Segmentation Analysis', fontsize=16, fontweight='bold')
        
        # 1. Risk Score Distribution
        axes[0, 0].hist(self.df['RiskScore'], bins=30, alpha=0.7, color='skyblue', edgecolor='black')
        axes[0, 0].set_title('Risk Score Distribution')
        axes[0, 0].set_xlabel('Risk Score')
        axes[0, 0].set_ylabel('Frequency')
        axes[0, 0].axvline(self.df['RiskScore'].mean(), color='red', linestyle='--', label='Mean')
        axes[0, 0].legend()
        
        # 2. Segment Distribution Pie Chart
        segment_counts = self.df['RiskSegment'].value_counts()
        colors = ['green', 'yellow', 'orange', 'red']
        axes[0, 1].pie(segment_counts.values, labels=segment_counts.index, autopct='%1.1f%%', 
                      colors=colors, startangle=90)
        axes[0, 1].set_title('Customer Distribution by Risk Segment')
        
        # 3. Risk vs Tenure
        risk_colors = {'Low Risk': 'green', 'Medium Risk': 'yellow', 'High Risk': 'orange', 'Critical Risk': 'red'}
        for segment in self.df['RiskSegment'].unique():
            segment_data = self.df[self.df['RiskSegment'] == segment]
            axes[0, 2].scatter(segment_data['tenure'], segment_data['RiskScore'], 
                             c=risk_colors[segment], alpha=0.6, label=segment)
        axes[0, 2].set_title('Risk Score vs Customer Tenure')
        axes[0, 2].set_xlabel('Tenure (months)')
        axes[0, 2].set_ylabel('Risk Score')
        axes[0, 2].legend()
        
        # 4. Monthly Charges by Risk Segment
        segments_order = ['Low Risk', 'Medium Risk', 'High Risk', 'Critical Risk']
        axes[1, 0].boxplot([self.df[self.df['RiskSegment'] == seg]['MonthlyCharges'] for seg in segments_order])
        axes[1, 0].set_title('Monthly Charges by Risk Segment')
        axes[1, 0].set_xticklabels(segments_order, rotation=45)
        axes[1, 0].set_ylabel('Monthly Charges ($)')
        
        # 5. Churn Rate by Risk Segment (if churn data available)
        if 'Churn' in self.df.columns:
            churn_by_segment = self.df.groupby('RiskSegment')['Churn'].apply(lambda x: (x == 'Yes').mean() * 100)
            churn_by_segment = churn_by_segment.reindex(segments_order)
            bars = axes[1, 1].bar(churn_by_segment.index, churn_by_segment.values, 
                                 color=['green', 'yellow', 'orange', 'red'])
            axes[1, 1].set_title('Churn Rate by Risk Segment')
            axes[1, 1].set_ylabel('Churn Rate (%)')
            axes[1, 1].tick_params(axis='x', rotation=45)
            
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                axes[1, 1].text(bar.get_x() + bar.get_width()/2., height,
                               f'{height:.1f}%', ha='center', va='bottom')
        else:
            axes[1, 1].text(0.5, 0.5, 'Churn data not available', ha='center', va='center',
                           transform=axes[1, 1].transAxes)
            axes[1, 1].set_title('Churn Analysis')
        
        # 6. Risk Segment Heatmap by Contract Type
        contract_risk_crosstab = pd.crosstab(self.df['RiskSegment'], self.df['Contract'], normalize='index')
        contract_risk_crosstab = contract_risk_crosstab.reindex(segments_order)
        sns.heatmap(contract_risk_crosstab, annot=True, fmt='.2f', cmap='YlOrRd', ax=axes[1, 2])
        axes[1, 2].set_title('Risk Segment Distribution by Contract Type')
        axes[1, 2].set_ylabel('Risk Segment')
        
        plt.tight_layout()
        plt.savefig('/home/runner/work/Portafolio/Portafolio/customer_risk_segmentation_analysis.png', 
                   dpi=300, bbox_inches='tight')
        plt.show()
        
        print("Visualizations saved as 'customer_risk_segmentation_analysis.png'")
    
    def generate_recommendations(self):
        """Generate actionable recommendations for each risk segment."""
        print("\n" + "="*60)
        print("STRATEGIC RECOMMENDATIONS BY RISK SEGMENT")
        print("="*60)
        
        recommendations = {
            'Critical Risk': [
                "🚨 IMMEDIATE ACTION REQUIRED",
                "• Deploy retention specialists for personal outreach",
                "• Offer special retention packages and loyalty rewards",
                "• Switch to annual payment plans with discounts",
                "• Provide premium customer support and dedicated account managers",
                "• Conduct exit interviews to understand pain points",
                "• Consider service upgrades or bundle modifications"
            ],
            
            'High Risk': [
                "⚠️ PROACTIVE INTERVENTION NEEDED",
                "• Implement targeted retention campaigns",
                "• Offer contract upgrade incentives (month-to-month to annual)",
                "• Provide additional service training and support",
                "• Send satisfaction surveys and act on feedback",
                "• Offer loyalty rewards and service credits",
                "• Monitor usage patterns for early warning signs"
            ],
            
            'Medium Risk': [
                "📊 MONITOR AND NURTURE",
                "• Regular check-in communications and newsletters",
                "• Offer service optimization recommendations",
                "• Provide educational content about service benefits",
                "• Monitor for changes in usage patterns",
                "• Offer moderate loyalty incentives",
                "• Cross-sell complementary services carefully"
            ],
            
            'Low Risk': [
                "✅ MAINTAIN AND GROW",
                "• Focus on upselling and cross-selling opportunities",
                "• Use as advocates for referral programs",
                "• Gather testimonials and case studies",
                "• Minimal intervention required",
                "• Standard communication cadence",
                "• Consider them for beta testing new services"
            ]
        }
        
        for segment, recs in recommendations.items():
            print(f"\n{segment.upper()}:")
            for rec in recs:
                print(f"  {rec}")
        
        return recommendations
    
    def export_results(self, filename_prefix='customer_risk_segmentation'):
        """Export segmentation results to CSV files."""
        print(f"\nExporting results...")
        
        # Export full dataset with risk scores and segments
        self.df.to_csv(f'/home/runner/work/Portafolio/Portafolio/{filename_prefix}_full_data.csv', index=False)
        
        # Export segment summary
        segment_summary = self.df.groupby('RiskSegment').agg({
            'customerID': 'count',
            'RiskScore': ['mean', 'std'],
            'tenure': 'mean',
            'MonthlyCharges': 'mean',
            'TotalCharges': 'mean'
        }).round(2)
        
        segment_summary.columns = ['Customer_Count', 'Avg_Risk_Score', 'Risk_Score_Std', 
                                  'Avg_Tenure', 'Avg_Monthly_Charges', 'Avg_Total_Charges']
        segment_summary.to_csv(f'/home/runner/work/Portafolio/Portafolio/{filename_prefix}_summary.csv')
        
        print(f"Results exported to:")
        print(f"  • {filename_prefix}_full_data.csv")
        print(f"  • {filename_prefix}_summary.csv")
        print(f"  • {filename_prefix}_analysis.png")
    
    def run_complete_analysis(self):
        """Run the complete risk segmentation analysis."""
        print("🎯 Starting Customer Risk Segmentation Analysis")
        print("="*60)
        
        # Load and prepare data
        self.load_and_prepare_data()
        
        # Calculate risk scores
        self.calculate_overall_risk_score()
        
        # Create segments
        self.create_risk_segments()
        
        # Analyze segments
        self.analyze_segments()
        
        # Generate visualizations
        self.generate_visualizations()
        
        # Generate recommendations
        self.generate_recommendations()
        
        # Export results
        self.export_results()
        
        print("\n✅ Customer Risk Segmentation Analysis Complete!")
        print("="*60)
        
        return self.df, self.segments


def main():
    """Main function to run the customer risk segmentation analysis."""
    # Initialize the segmentation system
    segmentation = CustomerRiskSegmentation('/home/runner/work/Portafolio/Portafolio/telco_customer_churn.csv')
    
    # Run complete analysis
    segmented_data, segments = segmentation.run_complete_analysis()
    
    return segmented_data, segments


if __name__ == "__main__":
    main()