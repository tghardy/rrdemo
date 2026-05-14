
## **III. The Five Core Assumptions**

For the results of a linear regression to be valid and "BLUE" (Best Linear Unbiased Estimator), five primary assumptions must be met:

| Assumption | Description | How to Check |
| --- | --- | --- |
| **Linearity** | The relationship between $X$ and $Y$ must be linear. | Scatter plots of $X$ vs. $Y$ or residuals vs. fitted values. |
| **Independence** | Observations must be independent of one another. | Common in time-series; checked via Durbin-Watson test. |
| **Homoscedasticity** | The variance of residual errors should be constant across all levels of $X$. | Residuals vs. Fitted plot (look for a "funnel" shape). |
| **Normality** | For valid hypothesis testing, the residuals should be normally distributed. | Q-Q plot or Shapiro-Wilk test. |
| **No Multicollinearity** | Independent variables should not be too highly correlated with each other. | Variance Inflation Factor (VIF). |