# Nassau Candy Factory Reallocation and Shipping Optimization

Live dashboard: https://kmcpoyfq6k2ajgt2v7uam7.streamlit.app

A decision-support system that predicts shipping lead time, simulates moving each product to a different factory, and recommends reassignments while checking distance and confidence risks.

## Data
10,194 orders (2024 to 2025) from Nassau Candy Distributor, with 15 products, 5 factories and customers in the US and Canada. Factory locations and the product-to-factory mapping come from the project brief. There are no missing values or duplicate rows.

## Method
1. **Data check and cleaning.** Raw lead time (Ship Date minus Order Date) came out at 904 to 1,642 days, which is impossible. The values fall into groups about 365 days apart, so the Ship Dates carry whole-year shifts. Removing each group's offset gives realistic lead times (Same Day about 0.4 days, Standard Class about 5.3 days). This corrected column, Lead Time Clean, is the model target.
2. **Features.** Product, factory, region, ship mode, units, sales, and the distance from factory to the customer's state (haversine, using approximate state centers).
3. **Models.** Linear Regression, Random Forest and Gradient Boosting, trained on 80% of the data and tested on 20%.
4. **Simulation.** For each product, the model predicts lead time at all 5 factories with the distance recalculated.
5. **Recommendation and risk.** Each move gets a verdict: Recommend, High risk (distance rises more than 5%), Low confidence (under 20 orders) or Keep current.

## Results
| Model | MAE (days) | RMSE (days) | R2 |
|---|---|---|---|
| Linear Regression | 0.926 | 1.106 | 0.621 |
| Random Forest | 0.937 | 1.166 | 0.578 |
| Gradient Boosting | 0.919 | 1.103 | 0.623 |

Gradient Boosting is the selected model.

## Key findings
- Ship mode explains almost all of the predictable lead time. Region, factory and distance have very little effect.
- Predicted lead time differs by under 0.1 days between factories for most products, which is smaller than the model error (about 0.9 days). Factory reassignment is a weak lever in this data.
- Only 2 of 15 products get a clear recommendation: Wonka Bar - Scrumdiddlyumptious and Wonka Bar - Nutty Crunch Surprise, swapping between Lot's O' Nuts and Wicked Choccy's (about 11% shorter distance).
- Seven products are high risk because the best factory is farther away, and three have too few orders to trust.

## Limitations
- The Ship Date shift had to be corrected, so lead times are reconstructed, not original.
- The data has no shipping cost or factory capacity, so distance is used as a cost proxy.
- Customer locations are state centers, not exact addresses.
- Three factories have very few orders.

## Dashboard modules
Factory Optimization Simulator, Recommendation Dashboard, Risk and Impact Panel, What-If Scenario Analysis, speed-versus-cost priority slider with a low-confidence filter, and live prediction by region and ship mode.

## Project structure
```
data/raw          original dataset
data/processed    cleaned data, simulation and recommendation tables
notebooks         01_eda.ipynb, 02_modeling.ipynb
models            saved Gradient Boosting model
reports           charts and model results
app.py            Streamlit dashboard
```

## Run locally
```
pip install -r requirements.txt
streamlit run app.py
```