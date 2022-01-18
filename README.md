[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-f059dc9a6f8d3a56e377f745f24479a46679e63a5d9fe6f495e02850cd0d8118.svg)](https://classroom.github.com/online_ide?assignment_repo_id=6731951&assignment_repo_type=AssignmentRepo)
# Coursework 1 

### Target audience

As this problem is widespread across Netflix users, our target audience should align closely with that of the platform. According to the Consumer & Media View Survey carried out by Nielsen in 2015, approximately 89% of Netflix users are young adults (aged 18-24), with a large skew aged between 25-39.

The following user persona exemplifies the target audience further:

![Persona Image](comp0034/comp0034-cw1/user_persona.png)


### Suggested web app

To address this problem, I suggest a solution which requests the user input of their movie genre preferences and time they have set aside for watching and returns a list of movies to match. However, if a user is really stumped for choice and has no genre preferences nor time limit, the app will show them a data visualisation highlighting the genres they are most likely to find entertaining and prompt them again for their genre preferences. In response, users can either select one of these genres and be shown a list of movies that match or they can decline to choose (by pressing the "Choose for me" button); in this case, the web-app would make a random selection of movies and visualise their entertainment value.

In line with our target audience's preference for internet streaming, the solution should come in the form of a web-app to maintain the same level of convenience Netflix users are used to in their streaming experience.

To ensure the solution is effective at solving the problem at hand, I suggest focusing on addressing the following data-focused questions. In brackets I also describe the statistical processes that could be used to solve each of these questions, using our data:


### Questions to be answered using the dataset

- *What combination of movies is the most entertaining to a user given specific preferences (their preferred genres & the ideal maximum length of marathon)?* - **Recommendation**
- *Is there a correlation between movie genre and movie popularity? What are the most popular movie genres?* - **Regression**
- *What are the most popular movies within each genre?* - **Regression**
- *Which movies fit into the category of the genres they'd like to watch?* - **Classification**
- *How many movies of this genre can they fit into their allotted marathon time?* - **Summation**


## Data preparation and exploration
### Data preparation

