import pandas as pd#

shopify = pd.read_csv("shopify_orders.csv")
paypal = pd.read_csv("paypal_payment.csv")
fb = pd.read_csv("facebook_ads.csv")

print("--- Messy Shopify Data ---")
print(shopify.head(), "\n")

print("--- Messy PayPal Data ---")
print(paypal.head(), "\n")

print("--- Messy Facebook Ads Data ---")
print(fb.head(), "\n")

print("---cleaning Shopify Data...---")
shopify['Date'] = pd.to_datetime(shopify['Date'], format='mixed').dt.strftime('%Y-%m-%d')

shopify['Gross_Revenue'] = shopify["Gross_Revenue"].str.replace('$', '', regex=False).astype(float)

print(shopify)
print("\nShopify Column Types:")
print(shopify.dtypes)

print("---cleaning PayPal Data...---")
paypal = paypal.drop_duplicates(subset=['TXN_ID'])

paypal = paypal.dropna(subset=['Shopify_ID'])

paypal['Shopify_ID'] = paypal["Shopify_ID"].astype(int)

print(paypal)

print("\n---cleaning Facebook Ads Data...---")
fb['Amount_Spent'] = fb['Amount_Spent'].fillna(0.0)
print(fb)


print("\n---Merging All Data...---")
merged_sales = pd.merge(shopify, paypal, left_on='Order_ID', right_on='Shopify_ID', how = 'inner')

final_data = pd.merge(merged_sales, fb, left_on='Date', right_on='Ad_Date', how = 'left')

final_data = final_data.drop(columns=['Shopify_ID', 'Ad_Date'])

print(final_data)

final_data.to_csv("clean_master_report.csv", index=False)
print("\nSuccess! 'clean_master_report.csv' has been generated")


import matplotlib.pyplot as plt
print("\n--- Generating Portfolio Charts... ---")
product_sales = final_data.groupby("Product")["Gross_Revenue"].sum()

plt.figure(figsize=(6, 4))
product_sales.plot(kind = 'bar', color = ['#4F46E5', '#0EA5E9'])
plt.title('Total Revenue by Product Category')
plt.xlabel('Product')
plt.ylabel('Revenue ($)')
plt.xticks(rotation = 0)
plt.tight_layout()
plt.savefig('Product_perfomance.png')
plt.close()

daily_trends = final_data.groupby('Date')[['Gross_Revenue', 'Amount_Spent']].sum()

plt.figure(figsize=(7, 4))
plt.plot(daily_trends.index, daily_trends['Gross_Revenue'], marker = 'o', label = 'Revenue ($)', color = 'green', linewidth = 2)
plt.plot(daily_trends.index, daily_trends['Amount_Spent'], marker = 's', label = 'Ad Spend ($)', color = 'red', linewidth = 2)
plt.title('Daily Marketing Performance (ROI Tracker)')
plt.xlabel('Date')
plt.ylabel('Amount ($)')
plt.grid(True, linestyle = '--', alpha = 0.5)
plt.tight_layout()
plt.savefig('marketing_roi_tracker.png')
plt.close()

print("Success! 'Product_perfomance.png' and 'marketing_roi_tracker.png' have been saved to your folder.")
