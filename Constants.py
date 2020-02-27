months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
emi_formula = '(self.principal_amount*self.rate_of_interest*(1+self.rate_of_interest)**self.tennure)/((1+self.rate_of_interest)**self.tennure-1)'
rate_of_interest_formula = 'self.interest_per_annum/(12*100)'