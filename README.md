# BackEndSkillsTest
### Prompt:
Within this directory is an extract of data we have compiled and cleaned in the course of our work that we obtained from the US Census Bureau. This dataset describes state populations and state-to-state migration flows from the decade between 2010 and 2019.

The Census Bureau classifies states into 9 geographical divisions, which are in turn classified into 4 regions. The file census_classification.csv describes these relationships. Each row represents one entity that has a level of one of (state, division, region) with a unique id. Each state and division row also has a parent_id which corresponds to the id of its parent one level up. These relationships can be used to traverse the resulting hierarchical tree.

Each row of data found in census_migration_data.csv describes the estimate of the amount of people who moved from one state (previous_state) to anothere state (current_state) in a given year between 2010 and 2019. This is also informed by a margin_of_error describing the range of what the true value of the estimate may be.

Finally, state_populations.csv gives the population of each state for each year within the observation period.

### Task 1: Aggregate Data
> Let's say once we have obtained this dataset, we are interested in first examining high-level trends of migration flows within the US. We need you to produce an aggregated dataset showing the summed estimates of people moving from a previous Census division to their current Census region for each year. You can drop margin_of_error for this task. The output for this task should be a CSV named aggregated_migration.csv with each row being a division-to-region pair for a given year. As you are aggregating fields from the state level, feel free to rename columns to something more accurate and descriptive as necessary.


### Task 2: Analyze Data
> Looking solely at rows in the raw data where the current_state is North Carolina, we need you to generate a CSV called nc_migration.csv where each row corresponds to a year and has additional columns answering the following questions:
> - Which state had the largest number of people move to North Carolina that year?
> - Which state had the largest proportion of its own population move to North Carolina that year?
> - How many states had at least 10,000 people move to North Carolina that year?
> - What percentage of people who migrated to North Carolina that year came from outside of the South Atlantic division?

> In the output file, it is fine to use state abbreviations when applicable instead of full names if more convenient. Name columns something descriptive but concise. You can also use the estimate field for all questions and do not need to incorporate margin_of_error in this task.


### Task 3: Build a Web API
> Write the code to run a web server (locally is fine) where a user can call a specific URL to perform a query. You are encouraged to use an existing framework (Flask, Django, Graphene, etc.) to simplify this.

> In addition to provided fields, we also want to generate lower- and upper-bounds for the estimates using the margin_of_error. These can be calculated by adding or subtracting margin_of_error from the estimate (with a floor at 0).

> Each row should return the following fields:
> - previous_state: 2-character state abbreviation
> - year
> - estimate
> - estimate_lb: estimate - margin_of_error
> - estimate_ub: estimate + margin_of_error

> The types of endpoints we want to build are as follows:
> - `/previous_state/<id>/`
> - `/previous_state/<id>/<year>/`
> - `/previous_division/<id>/`
> - `/previous_division/<id>/<year>/`


### Overview of my solution and approach:

For this project I chose to use MySQL, Flask, and Pandas since I already had some familiarity with them.

I started out creating the database and tables based on the csv files provided, making some changes to the structure and file names. I then initialized the tables:

- `mysql> CREATE TABLE state_pop (`
- `> id INT NOT NULL AUTO_INCREMENT,`
- `> state VARCHAR(5) NOT NULL,`
- `> year INT NOT NULL,`
- `> population INT NOT NULL,`
- `> PRIMARY KEY (id));`

After getting the tables configured and populated, I started out focusing on Task 2 and breaking the subproblems dwon into more simple queries, answering questions that would build towards answering the initial prompt:

ex: What percentage of people migrated to NC from each state each year?
- `mysql> SELECT m.previous_state, (m.estimate/p.population) percentage, m.year`
- `FROM migrations m`
- `INNER JOIN state_pop p`
- `ON m.previous_state = p.state AND m.year = p.year`
- `WHERE current_state='NC';`
I created a view based on the query above and answered similar questions until I either answered the initial prompt or was close enough to the answer where I knew I would be able to get the desired result using pandas and python.

After completing my initial queries, I chose to use Flask to build my API. I have more recent experience with Django, but it would have added more complexity than needed for this project. 

I read through some of the documentation for SQLAlchemy, but have no prior experience with it, so I ended up using mysql-connector-python as my driver for connecting to my database.
