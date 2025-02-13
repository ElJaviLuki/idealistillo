![Logo](idealistillo_logo.png)

Welcome to **Idealistillo** – an innovative tool designed to help both landlords and tenants navigate today’s challenging property market. With property prices soaring and the rental and purchasing markets becoming increasingly competitive, Idealistillo empowers landlords and tenants alike by providing actionable insights and data-driven solutions to inform business strategies and decisions.

## Why Idealistillo?

In a fast-paced and often unpredictable property market, whether you're a private landlord managing rental properties, a real estate agency, or a tenant searching for the right home, having access to real-time data and market trends is essential. Idealistillo provides a comprehensive solution for both property owners and tenants by analyzing the market, improving decision-making, and helping you stay ahead.

- **For Landlords:** Gain insights into pricing trends, property demand, and competitor strategies to optimize your rental or sale pricing, attract tenants, and make better investment decisions.
- **For Tenants:** Find the best properties based on your specific needs (price, location, type, etc.), get a better understanding of market trends, and make smarter decisions when choosing a home.
- **Advanced Filtering:** Customize your property search criteria to ensure that you are always focused on what matters most, whether you’re renting or purchasing.
- **Data-Driven Decisions:** Transform raw market data into strategic insights to help both landlords and tenants navigate the property market with greater efficiency.

## Features

- **Secure Authentication:** Ensures that your communications are secure with OAuth and HMAC-SHA256 request signing.
- **Custom Filter Builder:** Use the SearchFilterBuilder to set personalized criteria and analyze market data for specific property types, price ranges, locations, and more.
- **Optimized Experience:** Idealistillo helps both landlords and tenants simplify the search and analysis process by turning complex market data into actionable insights.
- **Open-Source Innovation:** Idealistillo is a contribution to solving real-world challenges in the property market, offering fresh ideas and solutions for both landlords and tenants.

## Installation

Clone the repository:

```bash
git clone https://github.com/eljaviluki/idealistillo.git
cd idealistillo
```

## Basic Usage

Here’s a simple example to get you started with property search and market analysis:

```python
from idealistillo import IdealistaClient, SearchFilterBuilder

# Initialize the client and authenticate
client = IdealistaClient()
client.start()

# Build a filter to search for rental or purchase properties based on criteria like price range, location, and type
filter = (
    SearchFilterBuilder()
    .set_operation('rent')  # or 'sell' for purchase
    .set_property_type('homes')
    .set_price_range(500, 1500)
    .set_location('Madrid')
    .build()
)

# Perform the search or analysis
results = client.search(filter)
print(results.json())
```

## The Current Property Market

The property market is increasingly complex, with rising prices and intense competition among both landlords and tenants. Landlords must adjust their strategies to remain competitive and attract quality tenants, while tenants must stay informed to make the best decisions on where to live and at what price. Idealistillo enables both groups to navigate these challenges by providing a tool that simplifies property search, pricing strategies, and market analysis.

## A Special Note to Idealista Recruiters

Dear Idealista recruiters, I understand the evolving nature of the property market and the demands on your work. I appreciate the opportunity to present this project. Idealistillo reflects a sincere effort to offer a solution that helps both landlords and tenants make smarter, data-driven decisions in an ever-changing market. I hope this project serves as an example of the fresh thinking that can bring value to the real estate industry.

## Contributing

Contributions are warmly welcome! If you have ideas or improvements for Idealistillo, please open an issue or submit a pull request. Together, we can make property market analysis more accessible and efficient for everyone.

## License

Idealistillo is released under the [MIT License](LICENSE).

---

Thank you for checking out Idealistillo. Let's work together to make property searching, pricing, and investment decisions more accessible, data-driven, and strategic for both landlords and tenants.
