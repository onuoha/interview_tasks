
You need to create an automated test suite that automatically tests basic operations of d3a.io. The tests should use an precreated test user, in order to login to the website and test some basic operations of the website. The tests for these operations need to be defined as separate test cases. 
There are 3 main testcases that need to be created here: 
1. Login testcase. Validate that a precreated user is able to login to d3a.io
2. (Depends on testcase 1) Create a Project. Validate that a logged in user is able to create a project from this page https://www.d3a.io/projects (the page is also accessible via a link to the left panel, second icon from the top). Validate that the project is listed correctly after being created.
3. (Depends on testcase 2) Create a simulation. Validate that, if the project in testcase 2 has been created successfully, a logged in user can create a simulation (button "New Simulation" in the project view). The simulation can be empty, does not need to have any special setup. Also validate that the simulation is listed correctly.  

The automated test suite can be created either using Cypress or Selenium (ideally in Javascript or Python).

Extra points for writing the testcases in Gherkin syntax (given/when/then).
