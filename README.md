# GoComet
# Testing.py uses chromedriver.exe to run it, please make sure your Chrome Version is 88.0.4324.190 (Official Build) (64-bit)
# Use of Selenium was kept to minimum because automated web browsing takes more time to run
# 1 Problem1.py take one search input in cmd and generate output file of .xlsx 
- <h2>Steps to run Problem1.py
- Enter input for item to be searched
- ![P1](https://github.com/Rishabhjaiswal0111/GoComet/blob/master/gocomet/img/img/p1.PNG)
- After some time an output file will be generated after the name of same search input of type .xlsx (eg for above input)
- ![P2](https://github.com/Rishabhjaiswal0111/GoComet/blob/master/gocomet/img/img/p2.PNG)
- <h2>*All title are Hyperlinked to the respected pages*

# 2 Problem2.py take search input, Number of product, Sort by(number), Min and Max price range and find related links and output it to cmd
- <h2>Steps to run Problem2.py
- ![P3](https://github.com/Rishabhjaiswal0111/GoComet/blob/master/gocomet/img/img/p3.PNG)
- <h2>*All the inputs have some default parameter set to it except search*

# 3 Problem4.py take search input and check first from flipkart and tries to match that product to amazon if found changes are made and output file of .xlsx if generate
- <h2>Steps to run Problem4.py
- Enter input that has to compared to
- ![P4](https://github.com/Rishabhjaiswal0111/GoComet/blob/master/gocomet/img/img/p4.PNG)
- Output of above is save in excel file (eg of above)
- ![P5](https://github.com/Rishabhjaiswal0111/GoComet/blob/master/gocomet/img/img/p5.PNG)

# 4 Problem 3 and 5 can be solved using different user_agent to make it seems like multiple devices from same ip is being requesting. Adding proxy to url request so that our ip does not get blocked or blacklisted. Using list of proxy will be more effective way and should to used with random user_agent. To make requests more human like must add some delay after one request. This method comes with price of time. Buying near by proxy should do the trick. Problems(1,2,4) were not solved using this method just to make it more faster.
