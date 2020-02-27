from tabulate import tabulate
from EmiCalculator import EmiCalculator
from Constants import months

class EmiEstimator():
	prev_principal_amount = None
			
	def __init__(self):
		prev = input('Do you have an existing loan (Y/N): ')
		
		if prev[0].strip().lower() == 'y':
			self.prev_principal_amount = float(input('Previous loan amount: '))
			self.prev_interest_per_annum = float(input('Previous loan rate of Interest: '))
			self.prev_tennure = int(input('Previous loan tennure: '))
			self.prev_month = int(input('Starting month (number): '))
			self.prev_year = int(input('Starting year (YYYY): '))
		
		self.principal_amount = float(input('Current Loan amount: '))
		self.interest_per_annum = input('Current expected rate of Interest (comma "," seperated for multiple values): ').strip().split(',')
		self.tennure = int(input('Number of months: '))
		self.start_year = int(input('Planned year range start (YYYY): '))
		self.start_month = int(input('Expected start month range to begin estimate(number): '))
		self.end_year = int(input('Planned year range end (YYYY): '))
		self.end_month = int(input('Expected end month range to end estimate(number): '))

		self.emiCalculator = EmiCalculator()
		
		
	def create_estimate(self):
		estimate_list = []
		prev_payment_list = []
		prev_tennure_list = []
		number = 1
		if self.prev_principal_amount:
			self.emiCalculator.set_data(self.prev_principal_amount, self.prev_interest_per_annum, self.prev_tennure, self.prev_month, self.prev_year)
			prev_emi, prev_payment_list, prev_tennure_list = self.emiCalculator.calculate_emi()
		
			estimate_list.append({'month' : self.prev_month,
								  'year' : self.prev_year,
								  'loan_amount' : self.prev_principal_amount,
								  'schedule' : prev_payment_list,
								  'tennure' : self.prev_tennure,
								  'rate_of_interest' : self.prev_interest_per_annum,
								  'emi' : prev_emi,
								  'title' : 'Existing',
								  'outstanding' : '0',
								  })
		
		quote_list = self.get_quote_list(prev_payment_list, prev_tennure_list)

		for quote in quote_list:
			for interest in self.interest_per_annum:
				estimate_obj = {}
				estimate_obj.update(quote)
				estimate_obj['rate_of_interest'] = float(interest)
				self.emiCalculator.set_data(estimate_obj['loan_amount'],
											estimate_obj['rate_of_interest'],
											estimate_obj['tennure'],
											months.index(estimate_obj['month'])+1,
											int(estimate_obj['year']))
				emi, payment_list, _ = self.emiCalculator.calculate_emi()
				estimate_obj['emi'] = emi
				estimate_obj['schedule'] = payment_list
				estimate_obj['title'] = 'Estimate {}'.format(str(number))
				number+=1
				estimate_list.append(estimate_obj)
		
		return estimate_list
		

	def get_quote_list(self, prev_payment_list, prev_tennure_list):
		quote_list = []
		current_start_month = self.start_month - 1 if self.start_month <= 12 and self.start_month > 0 else 0
		current_end_month = self.end_month - 1 if self.end_month <= 12 and self.end_month > 0 else 0
		for year in range(self.start_year, self.end_year+1):
			for month in self.get_month_list(year):
				quote_obj = {}
				quote_obj['month'] = month
				quote_obj['year'] = str(year)

				if quote_obj in prev_tennure_list:
					index = prev_tennure_list.index(quote_obj)
					loan_amount = prev_payment_list[index]['remaining_amount'] + self.principal_amount
					quote_obj['outstanding'] = prev_payment_list[index]['remaining_amount']
				else:
					loan_amount = self.principal_amount	
					quote_obj['outstanding'] = 0
					
				quote_obj['loan_amount'] = loan_amount
				quote_obj['tennure'] = self.tennure
				quote_list.append(quote_obj)
		return quote_list
		
	def get_month_list(self, year):
		if self.start_year == self.end_year:
			return months[self.start_month-1:self.end_month]
		elif year == self.start_year:
			return months[self.start_month-1:]
		elif year == self.end_year:
			return months[:self.end_month]
		else:
			return months
			
	def dummy(self):
		self.prev_principal_amount = 927469
		self.prev_interest_per_annum = 12
		self.prev_tennure = 60
		self.prev_month = 5
		self.prev_year = 2019
	
		self.principal_amount = 1000000.0
		self.interest_per_annum = ['11','11.5','12']
		self.tennure = 60
		self.start_year = 2021
		self.start_month = 6
		self.end_year = 2021
		self.end_month = 12
		
if __name__ == '__main__':
	emiEstimator = EmiEstimator()
	#emiEstimator.dummy()
	estimate_list = emiEstimator.create_estimate()
	for estimate in estimate_list:
		payment_list = estimate['schedule']
		print('\n')
		print('-'*150)
		print('Title: {}'.format(estimate['title']))
		print('Loan amount of {} with outstanding amount of {} for the rate of interest of {} with tennure {} with EMI: {}'
																							.format(estimate['loan_amount'],
																									estimate['outstanding'], 
																									 estimate['rate_of_interest'],
																									 estimate['tennure'],
																									 estimate['emi']))
		print(tabulate([[str(item['serial']),
						str(item['month']),
						str(item['year']),
						str(item['emi']),
						str(item['interest']),
						str(item['principal_amount']),
						str(item['remaining_amount'])] for item in payment_list],
						headers=["#", "Month", "Year", "Emi", "Interest", "Principal Amount", "Remaining amount"], 
						tablefmt='psql'))
		print('-'*150)
	
