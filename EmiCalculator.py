from tabulate import tabulate
from Constants import months, emi_formula, rate_of_interest_formula 

class EmiCalculator():
	
	def get_data(self):
		self.principal_amount = float(input('Loan amount: '))
		self.interest_per_annum = float(input('Rate of Interest: '))
		self.tennure = int(input('Number of months: '))
		self.month = int(input('Starting month (number): '))
		self.year = int(input('Starting year (YYYY): '))

	def set_data(self, principal_amount, interest_per_annum, tennure, month, year):
		self.principal_amount = principal_amount
		self.interest_per_annum = interest_per_annum
		self.tennure = tennure
		self.month = month
		self.year = year
		
	def calculate_emi(self):
		payment_list = []
		tennure_list = []
		
		self.rate_of_interest = eval(rate_of_interest_formula)
		emi = round(eval(emi_formula))

		rem_amount = self.principal_amount
		current_month = self.month - 1 if self.month <= 12 and self.month > 0 else 0
		current_year = self.year
		for i in range(self.tennure):
			payment_obj = {}
			payment_obj['serial'] = i+1
			payment_obj['month'] = str(months[current_month])
			payment_obj['year'] = str(current_year) 
			if current_month == 11:
				current_month = 0
				current_year = current_year + 1
			else:
				current_month += 1
			tennure_list.append({'month' : payment_obj['month'], 'year' : payment_obj['year']})
			payment_obj['emi'] = emi
			payment_obj['interest'] = round(rem_amount * self.rate_of_interest)
			payment_obj['principal_amount'] = round(emi - payment_obj['interest'])
			rem_amount = round(rem_amount - payment_obj['principal_amount'])
			rem_amount = rem_amount if rem_amount > 0 else 0
			payment_obj['remaining_amount'] = rem_amount 
			payment_list.append(payment_obj)
			
		return emi, payment_list, tennure_list
	
if __name__ == '__main__':
	emiCalculator = EmiCalculator()
	emiCalculator.get_data()
	emi, payment_list, tennure_list = emiCalculator.calculate_emi()
	print('Your Emi is: '+ str(emi))
	print(tabulate([[str(item['serial']), str(item['month']), str(item['year']), str(item['emi']), str(item['interest']), str(item['principal_amount']), str(item['remaining_amount'])] for item in payment_list], headers=["#", "Month", "Year", "Emi", "Interest", "Principal Amount", "Remaining amount"], tablefmt='psql'))
	print(tennure_list)
