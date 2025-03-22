# 21.03.
Attempting to create a scraper for companies-marketcap. Issue is that the URL has the company name in a random format. I believe my best bet is to use the search function of the site to find the page I want to scrape, because searching for the ticker of a company does return the company.
I tried some methods to scrape the search results using the lists I already have for the payload, but the results are too random for me to work with.
I decide to invest the time to manually extend my list of companies with the marketcap url, then I can scrape the data

while collecting the data, I noticed that the marketcap isn't fully transparent. It's unclear how the marketcap was sourced to begin with, and sometimes the website claims to show the marketcap of a holding or just a company whereas I have a group on my list (UBS for example). I'll keep the data and assume they refer to the same entity
Another issue is that the marketcap is in USD, most of my data is in local currency (CHF)

After ~2 hours of pasting URLs into my list, I have my marketcap csv in my folder
as mentioned the data is is USD, and it's formatted as e.g. $10M instead of full numbers. I'll need to clean that up.

The clean up is done, I have a list of companies with their marketcap in USB. I'll need to add that data to the main dataset

# 22.03.
today i'll add the marketcap data to the main dataset. I can use the symbol and year to find where to add the marketcap. Once that's done I can start with the analysis, by figuring out the altman z-score.

I found that some columns are duplicated in my full dataset. It's unclear why, and drop_duplicates doesn't recognize them.
    there were some duplicate sources in the data, after deleting those and recreating the dataset, the duplicates are gone
