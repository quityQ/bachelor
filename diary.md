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

# 28.03.
During the altman analysis I ran into 2 issues
    1. there are still some duplicates (ex. STLN), this time it's because the same company is listed in the reegular and distressed list. I'll remove it from the regular list, since it's planning to leave the stock market in 2025, and recreate the dataset.
    2. Some of the altman results are ridiculously extreme, those probably must be removed, but it's probably worth to check the data for edge cases, if not just to find a save threshold for a cutoff point
I created correlatoin matrices to get an overview of the data, but I don't think that it gave me a lot of insight.

# 04.04.
I cleaned up the matrices from last week a little bit. I think the biggest insight that gave me was that I really only have 2 valid "distressed" companies in my dataset. For each model I'm building I should use the full dataset and the dataset with the outliers removed (using 1 standard deviation). 
Today I want to start with the logistic regression model. I'll use Introduction to statistical learning as a reference.

After some tinkering I managed to run a logistic regression model, however in ran into a PerfectSeparationWarning. This seems to be somewhat common, so I will try to fix it.

I wasn't able to fix the warning, but after reading a little about it. I think I could attempt to remove some of the variables, and see if I get better results like that. I won't be using another model, as it's recommended, mainly becuase the recommended model isn't baked into the libraries I'm using.

# 05.04.
I cleaned up the logistic regression, so that i wouldn't have to use a pandas mapper. The results didn't change, so for today I'll move on to another model, I'll ask Pasquale if there is an obvious fix to the logistic regression, or if this just might be my result.

I started with the tree model, which ended up being fairly straightforward to implment. It also resulted in a model with very high accuracy. I believe that to be suspicious, but even with validation it still is very strong. Not sure what to make of this result, maybe the approach with the zscore is faulty.

# 11.04.
I had an email exchange with Paquale about my issues. Here are the next steps I want to take:
- Analyze pairwise correlations, and find features with high correlations, those are the features that can be ignored during anlysis
- Create distressed dummy observations using SMOTE (?) or other methods
- check the outliers more carefully, and try to understand why they're outliers

Using SMOTE was fairly easy, but I didn't check the results manually, I just saw that the balance in my dataset was 1:1 now. Maybe there are settings to create less dummy variables, because having half the dataset be a dummy variable seem excessive. This alone however didn't fix the issues I was facing last week.
To deal with the multicollinearity/PerfectSeparationWarning I used VIF to analyze the collinearity of features. The issue is that about 90% of the features show a high VIF value, and just removing the features with infinite VIF, didn't help much with the model.
This might be a sign that a logistic regression isn't a good fit for my data set. I want to discuss theese findings with Pasquale if possible. Before I should continue the analysis of the logistic regression, now that I have a model that looks decent.

