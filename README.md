# smart trading

a website that helps investors to look out for upcoming stocks and check the stocks of thie choice.
in addition there is a trading bot based on the moving average algorithm.

video of activating the app - https://youtu.be/RLrIyyWwI3U

in this project i: calculated which stocks are worth to invest in usimg mathematical formulas based on the data of the stock, i scraped data from the internet, i built a website, 
i used sentiment anylasise to get the most strendy stocks talked about on reddit foroums, i used the google trends data to check if the price of the stock is related to the price of the stocl,
and i also built a trading bot based on the moving average algorithm.

i built a website using django in python. coded in javacript, css.

first main aspect is the top 10 stocks the program reccomends. firstly i take a list from TASE (tel aviv stock exchange) of all stocks that are traded over there - 
and than with a formula i calculate each stocks value (by data of the companies cash flow, market cap..) 
also i use web scraping to get the data about the stocks. i go to yahoo finance and get all the data in the web and i find the data in the javascript function and identify where is the json data and from there i extract the data needed

the second main aspect is the website itself.

the third main aspect is the reddit sentiment analyasise. i took posts from reddit foroums that talk about stocks and i saved for each stock the post's that talk about it.
after that i used a dictionary to define which words are bad, and which are good - and with that i got the most talked about stocks.
 
the last main aspect of the project is the trading bot - which i didnt include in the webste because he isnt percise enough.

more features: i also built a website and used google trend data.
