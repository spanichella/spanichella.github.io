
#F-Index:  funding / number of years after the PhD 
EUR_exchange<- 0.9259
ARIES_Project_CHF<-500000
SURF_Project_CHF<- 349926
COSMOS_project_EUR<- 770000
funding_in_CHF<- ARIES_Project_CHF+SURF_Project_CHF+COSMOS_project_EUR/EUR_exchange
print(funding_in_CHF)
funding_in_EUR<- funding_in_CHF * 0.9259
print(funding_in_EUR)

H_Index<- 29
years_after_the_PhD<- 7 

#F-Index:  (funding / 1000)  / number of years after the PhD 
# 
FIndex_CHF<- funding_in_CHF / 1000 / years_after_the_PhD
FIndex_EUR<- funding_in_EUR / 1000  / years_after_the_PhD
print(FIndex_CHF)
print(FIndex_EUR)

#FH-Index: (funding/1000)  / h-index 
FHIndex_CHF<- funding_in_CHF / 1000 / H_Index
FHIndex_EUR<- funding_in_EUR / 1000 / H_Index
print(FHIndex_CHF)
print(FHIndex_EUR)

  