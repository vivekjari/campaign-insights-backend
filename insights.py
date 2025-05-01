# insights.py
import pandas as pd

def generate_insights(df):
    insights = []

    # Basic correlation
    corr = df[['sentiment', 'ctr', 'cvr', 'conversions', 'spend']].corr()
    sentiment_corr_conv = corr.loc['sentiment', 'conversions']
    if sentiment_corr_conv > 0.3:
        insights.append("Higher sentiment seems to be positively influencing conversions.")
    elif sentiment_corr_conv < -0.3:
        insights.append("Negative sentiment might be hurting conversions.")
    else:
        insights.append("Sentiment doesn’t have a strong effect on conversions.")

    # CTR spikes
    avg_ctr = df['ctr'].mean()
    high_ctr_days = df[df['ctr'] > avg_ctr * 1.5]
    if not high_ctr_days.empty:
        dates = ", ".join(high_ctr_days['date'].dt.strftime('%b %d'))
        insights.append(f"Your click-through rate (CTR) spiked on: {dates}.")

    # CVR anomalies
    avg_cvr = df['cvr'].mean()
    very_high_cvr = df[df['cvr'] > avg_cvr * 2]
    if not very_high_cvr.empty:
        dates = ", ".join(very_high_cvr['date'].dt.strftime('%b %d'))
        insights.append(f"Crazy high conversion rates spotted on: {dates}.")

    # Spend vs conversions
    spend_corr = corr.loc['spend', 'conversions']
    if spend_corr > 0.3:
        insights.append("More spend is generally leading to more conversions.")
    elif spend_corr < -0.3:
        insights.append("Higher spend is not translating into better conversions.")
    else:
        insights.append("Spend and conversions don’t seem very connected.")

    # ROAS
    df['roas'] = df['conversions'] / df['spend']
    high_roas = df[df['roas'] > 3]
    if not high_roas.empty:
        dates = ", ".join(high_roas['date'].dt.strftime('%b %d'))
        insights.append(f"Your ROAS was high on: {dates}.")

    return insights

