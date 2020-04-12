## Database & Web Info
* PostgreSQL account: 
* Web URL:

## Features
In this web application, we built a website that allows users to search for company and job information. The users can also read and post comments and ratings about those companies and jobs. 

* **Company Listings** and **Job Listings**: The former feature allows users to see the name and industry of all of the companies in the database, and the later allows users to see the job title and company name of all available job positions. These two functions are new features that are not included in the part 1 proposal, but we think it might be a helpful to first let the users have a general idea of what type of companies and positions are available on our website.
* **Company Search**: This feature allows users to input a company name (does not have to be exact), and the website will display company information (Company Name, City, State, Company Description, Company Size, Average Salary) and other user's comments and ratings on the company (Username, Comment, Rating). This feature is an implementation of what we proposed in part 1.
* **Job Search**: This feature allows users to search for a job position that they are interested in (does not have to be exact), and the website will display job information (Job Title, Company Name, Job Description), other users' job reviews (User Name, Start Time of the Job, Job Rating, Job Comment) as well as their comment on the interview process (Interview Date, Difficulty Level, Question Asked). This feature is an implementation of what we proposed in part 1.

## 2 Most Interesting Web Pages
One of the web page that requires the most database operations is the *Job Search* feature. It is complicated because of the amount of tables that are involved in this method. As you can see from above, the *Job Search* function returns a lot of different information including job information, job reviews and interview reviews, which is separated in 6 entity and relationship tables. Further more, the 'Interview Question' attribute is a multivalue attribute in the 'Interview Review' table, so it has its own table that stores different interview questions with respect to each interview. Therefore, we need to strategically join all of these table to get the correct information that the user wants.
