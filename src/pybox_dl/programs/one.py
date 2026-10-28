import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

X = np.array([1, 2, 3, 4, 5, 6]).reshape(-1, 1)
y = np.array([30000, 35000, 40000, 45000, 50000, 55000])

model = LinearRegression()
model.fit(X, y)
y_pred = model.predict(X)

print("Slope (Coefficient):", model.coef_[0])
print("Intercept:", model.intercept_)

experience = np.array([[7]])
predicted_salary = model.predict(experience)
print("Predicted Salary for 7 years of experience:", predicted_salary[0])

plt.scatter(X, y, color='blue', label='Actual Data')
plt.plot(X, y_pred, color='red', label='Regression Line')
plt.xlabel("Years of Experience")
plt.ylabel("Salary")
plt.title("Simple Linear Regression")
plt.legend()
plt.show()
