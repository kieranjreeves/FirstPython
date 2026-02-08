# Define constants
regular_rate = 20.0
overtime_rate = 30.0
regular_hours_limit = 40

# Input: Number of hours worked
hours = float(input("Enter the number of hours worked this week: "))

# Calculate pay
if hours <= regular_hours_limit:
    total_pay = hours * regular_rate
else:
    regular_pay = regular_hours_limit * regular_rate
    overtime_hours = hours - regular_hours_limit
    overtime_pay = overtime_hours * overtime_rate
    total_pay = regular_pay + overtime_pay

# Display result
print(f"Weekly paycheck: ${total_pay:.2f}")
