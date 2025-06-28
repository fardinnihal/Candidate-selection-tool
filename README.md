** HR Applicant Selector for Restaurant Franchise**

This script helps automatically select the best applicant for an interview based on:
- Previous workplace (priority-based)
- Role type (role-based filtering)
- Age (younger preferred)
- Experience (more preferred)

It uses `scikit-learn` to simulate a regression model that predicts suitability scores based on past data.

 How to Use

1. Install dependencies:
   ```bash
   pip install -r requirements.txt

Place your applicant data in restaurant_applicants.xlsx with the following columns:

Name

Previous Workplace

Age

Experience

Role

Now,
Run the script.
Output : The person selected for interview is {Name}


