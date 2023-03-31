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


## Overview of my solution and approach:

For this project I chose to use MySQL, Flask, and Pandas since I already had some familiarity with them. That said, at the time of this challenge I had not done much in Python for a year prior to this and had just recently set up MySQL on my computer. I had not made any SQL queries in well over a year, though, so I was refamiliarizing myself with SQL as I went along. I additionally had not done anything with Flask in a while (I was working primarily in Java for the last year). I wanted to demonstrate my ability to quickly get back up to speed on these tools, though.

I started out focusing on Task 2 & 3 and writing my SQL queries. I created my database and tables, populated them, and then started making queries directly through a MySQL shell. After I had most of the queries I'd need, I focused on setting up the Flask API since I knew I'd need that for Task 3. I created my endpoints and chose to also create endpoints for Tasks 1 & 2 so all tasks could have a similar structure. I then used my SQL queries to retrieve the data for the various API endpoints.

Example of initializing the tables:

- `CREATE TABLE state_pop (`
- `id INT NOT NULL AUTO_INCREMENT,`
- `state VARCHAR(5) NOT NULL,`
- `year INT NOT NULL,`
- `population INT NOT NULL,`
- `PRIMARY KEY (id));`

For the SQL queries, I started out answering questions that would build towards answering the initial prompts:

ex 1: 	Select all states and their region
- `SELECT s.abbrv, s.census_id, s.parent_id, d.parent_id`
- `FROM census_states s`
- `LEFT JOIN regions_and_divisions d`
- `ON s.parent_id = d.census_id;`

ex 2: Sum the estimate of people who moved to a particular region in a given year
- `SELECT SUM(m.estimate)`
- `FROM migrations m`
- `WHERE m.year = 2010 AND m.current_state IN (`
- `SELECT abbrv `
- `FROM state_div_reg`
- `WHERE reg_id = 'R1');`

ex 3: What percentage of people migrated to NC from each state each year?
- `SELECT m.previous_state, (m.estimate/p.population) percentage, m.year`
- `FROM migrations m`
- `INNER JOIN state_pop p`
- `ON m.previous_state = p.state AND m.year = p.year`
- `WHERE current_state='NC';`

I answered similar questions until I either answered the initial prompt or was close enough to the answer where I knew I would be able to get the desired result using pandas and python.

### Routes:
- `/task1/`
- `/task2/<state>/`
- `/previous_state/<id>/`
- `/previous_state/<id>/<year>/`
- `/previous_division/<id>/`
- `/previous_division/<id>/<year>/`
- `/migrationto/<region>/<year>/`
