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

# 12.04.
Today I want to continue with the logistic regression analysis. I just want to get all results by the book. Then continue with the tree/forest model.

I managed to get a confusion matrix and roc curve for the current model. The results seem good, but this is to be expected since I never split the data into a training and test set. 
I wanted to add the finding to the main analysis report, I wanted to add some additional information about the data, since I originally just uploaded it. I think explaining some of the data will help the understand the decisionmaking later down the line. How ever, while trying to improve the creation of datasets a little (there is an unccessary index in the main dataset) I ran into an issue with the marketcaps using large numbers, that python can't handle natively. It's werid that I didn't run into this issue before, but I those datasets were created a while ago, when I was using the latest version of pandas. After started with the statistical analysis I had to downgrade some of the dependencies. The fix wasn't difficult, there is a decimal library that helps with dealing with large numbers. 

# 17.04.
For the VIF analysis I had the idea to use standardized data, with the hopes of getting better results. However the results were pretty much the same as with the non-standardized data. I assume that this means that the data isn't at fault to create the extremely high VIF values, but rather the these features do just how high collinearity. 
While during test run I just recalculated the VIF after dropping the "infinite" values, and then using whatever remained below 10 for the new logisttic regression; I decided to take an (manual) iterative approach this time, by removing features one by one, until I reached a satisfying number of features below 10. This iterative process proved to be better, because it actually did leave more features above 10.
I been thinking about writing a piece of code to do that iterative process for me, incase I want to redo it for different cases, or for slightly different results, as it's fairly time intensive now. (each re-run takes about 30s with copying the name and calc the vif again)

# 20.04.
After the VIF analysis I ran some logistic regression models, those were better than the previous models, but I still wasn't happy with the results. After talking to Pasquale, he suggested to continue to do model selection, and maybe define a new target to use instead of using "distressed" so that I have a better balanced dataset.

# 25.04.
I started with defining a new target "unhealthy" using the zscore as a base and calling any observation a zscore lower than 3 "unhealthy". This resulted in a well balanced datset with almost a 50/50 split. I also decided to only use the 3rd standard deviation dataset going forward. It's still large, more complete, and outliers have been removed. At the very end I could always do another regression with the full dataset for comparison, but using a stable, balanced set makes it easier to find a good model.
I decided to automate the VIF analysis by moving the code into a function, this seems to be easier than redoing the manual steps again with the new dataset. 

at the end of the day I had a logreg model with decent results. I created a second model after splitting the data into a training and test set. The results ended up spightly worse. The next step would be to continue with other models (forest then SVM).

# 28.04.
continued a bit with the forest model. Didn't run into manny issues, but also couldn't get too much done today timewise

# 02.05.
today I want to continue with the forest model. I'll look to evaluation methods and then start on the actual analysis/report. 
Then perhaps I can create a tree based model using bagging (as a comparison, and to show have some visualization of what a single tree looks like).

Then I could continue with the SVM model, but I think it's time to put my findings into proper writing.