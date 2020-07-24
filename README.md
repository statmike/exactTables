# exactTables

Exact Tables focuses on recreating contingency tables from statistical information.

If you know 10% of people are left-handed, then you know that the other 90% are presumed right-handed.  With only two possible outcomes, the reduced information from this percentage is enough to complete the whole picture.

What happens when you get an average score from a rating scale, like the number of stars on a product review?  Perhaps the stars are {1, 2, 3, 4, 5}, and you know the average is 3.4 after 45 reviews.  What combinations of 45 ratings in the categories {1, 2, 3, 4, 5} could yield an average of 3.4?  What if you allow for non-responses?

This code returns all the combinations that yield a target statistic.  The inputs are:
* N = the number of ratings
* C = the number of response levels
* inczero = True/False for allowing 0 ratings (this would mean non-response and would not count towards the target evaluation)
* target = the mean of the responses.

## Computation Considerations
This seems like a trivial challenge.  Just cycle through the combinations, check for a match, return matches.  The computation challenge is that this becomes an enormous sequence quickly.  With 100 ratings in 6 categories, this is a binomial coefficient: (100+6-1) CHOOSE (6-1).  That's 96,560,646 combinations to evaluate!

This code detects the number of computing cores (virtual) on the local machine and creates thread vectors for each.  These vectors have start and end specifications for the combinations that achieve approximate balance across the available compute.  If you have a cluster with much more compute then this number can be changed.  It can be helpful to manually adjust this number and map out run times for your environment. 

The multiprocessing module runs each thread vector on a separate process. Quickly scale up to multiple machines by using the Fiber module.

Creating the thread vectors without cycling through all the combinations is done with combinatorics and a recursive function that loops through the high-level combination groupings, only drilling deeper when needed to create balance across the desired number of threads.  Very efficient!

Each thread loops through its allocation of combinations. NumPy arrays get used to collect combinations and then evaluate all together with vector math for efficiency.

# Tools
I picked Python for this.  It's widely available, easy to drive, and connects to many excellent computational infrastructures. 

Python 3.8+, with these modules
* math (comb function introduced in Python 3.8)
* time
* multiprocessing (included in Python since 2.6)
* NumPy

To scale this work, I prefer using the [UBER Fiber module](https://uber.github.io/fiber/). It's API makes putting this code into a Kubernetes cluster very simple. 

# Continued Development
A list of features in development
* provide examples on single machines and clusters
* make missing values an option, currently this code uses the first category as missing by default.  That means the first category is "0" and does not impact the mean calculation.
* display summary of likely distributions
* re-evalute a list of matches for additional ratings and new target
* more efficient algorithm for choosing combination ranges.  Currently, every possible combination gets evaluated.  For a given target, there are combination ranges that can be avoided altogether.
* provide different target types besides mean
* expand to 2-way tables
* package the project
* expand to n-way tables

