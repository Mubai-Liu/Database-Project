## Database & Web Info
* PostgreSQL account: ml4407    Password: 5974
* Web URL: http://35.237.141.253:8111/

## Features
In this web application, we built a website that allows users to search for company and job information. The users can also read and post reviews about those companies and jobs. 

* **Account Login** and **Account Registration**: For our website, user has to have an account to view all the available information. The former feature allows users to login to their existing accounts (with Username and Password), and the latter allows new users to fill out their personal information (Username, Password, Email, City, State, Degree) and register for new accounts. These two features are implementations of what we proposed in part 1.

* **Company Listings** and **Job Listings**: The former feature allows users to see the name and industry of all of the companies in the database, and the latter allows users to see the job title and company name of all available job positions. These two functions are new features that are not included in the part 1 proposal, but we think it might be helpful to first let the users have a general idea of what type of companies and positions are available on our website.

* **Company Search**: This feature allows users to input a company name (does not have to be exact), and the website will display company information (Company Name, City, State, Company Description, Company Size, Average Salary) and other user's comments and ratings on the company (Username, Comment, Rating). This feature is an implementation of what we proposed in part 1.

* **Job Search**: This feature allows users to search for a job position that they are interested in (does not have to be exact), and the website will display job information (Job Title, Company Name, Job Description), other users' job reviews (User Name, Start Time of the Job, Job Rating, Job Comment) as well as their comment on the interview process (Interview Date, Difficulty Level, Question Asked). This feature is an implementation of what we proposed in part 1.

* **Similar Company Recommendation**: This feature allows users to get information of companies similar to the company being searched. When the user input a company name, the feature will return companies that are in the same industry as the one being searched, and display the company's information. This feature is an implementation of what we proposed in part 1.

* **Add Company Review**: This feature allows users to reivew on companies that they worked at. Users will input their usernames, company names, comments and ratings, and the reviews will be added and displayed with the company information. This feature is an implementation of what we proposed in part 1.

* **Add Job Review**: This feature allows user to review on a specific job position at a company. Users will input their username, job title, company name, job start time, comment and ratings, and the reviews will be added and displayed with the job information. This feature is an implementation of what we proposed in part 1.

## Two Most Interesting Web Pages
1. One of the web page that requires the most database operations is the *Job Search* feature. It is complicated in terms of the amount of tables that are involved in this method. As you can see from above, the *Job Search* function takes in a job title, and returns a lot of different information including job information, job reviews and interview reviews, which is separated in 6 entity and relationship tables. Further more, the 'Interview Question' attribute is a multivalue attribute in the 'Interview Review' table, so it has its own table that stores different interview questions with respect to each interview. Therefore, we need to strategically join all of these table to get the correct information that the user wants.

2. Some other interesting features are the general *Review* features. First of all, they are different from some other features in the sense that they are addition methods that insert new information into existing tables. The user will input his/her company or job information (username, job title, company name, comment, rating, etc), then the system will append the informatoin to the corresponding 'Review' table, and the table will auto-assign a unique id for the new review (primary key). The system will then find the company id correponding to the entered company name, and add the company-review or job-review relationship to the 'has_review' relationship table.
