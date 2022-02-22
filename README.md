[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-f059dc9a6f8d3a56e377f745f24479a46679e63a5d9fe6f495e02850cd0d8118.svg)](https://classroom.github.com/online_ide?assignment_repo_id=6731951&assignment_repo_type=AssignmentRepo)
# Coursework 1 

## Purpose and Target Audience

My app, NetPicks, intends to offer a solution to streaming site users who suffer from “decision fatigue”: that is a phenomenon describing users’ struggle to choose, which is exacerbated by having more options they have to choose from. What’s the point in having thousands of content options on sites like Netflix and Amazon Prime if that makes it even harder to choose one?

The app is intended for use in tandem with Netflix, although we intend to expand its scope to other streaming platforms assuming it’s successful within the market. It’s targeted at young adults between the ages of 18 and 24 (as this demographic makes up 89% of the overall Netflix user base, according to a 2015 survey) and aims to create effective visualisations which empower users to make more informed and accurate choices on what to stream. 

The following user persona exemplifies the target audience and potential use cases of NetPicks:

![Persona Image](user_persona.png)

To address the “decision fatigue” issues widely posed by streaming platforms, NetPicks will act as a recommender engine which takes the input of a user’s genre preferences and the maximum amount of time they have to spend watching Netflix and returns a couple of visualisations on the viewing stats for different movies that match these. 

Thus, by going one step further than what’s currently offered on streaming platforms, in allowing for more than one genre preference and maximum time to be taken into consideration, and providing users with statistics on other viewers’ ratings of the movies that match these (such as popularity and average vote), NetPicks will help take out some of the guesswork and misdirection involved in users’ decision-making. 

For the app to achieve its intended purposes as described, the visualisations created therein aim to address the following questions:

1. *What are the most popular/highest scoring movies that match a user’s given preferences (their preferred genres and/or the maximum length of time they have to spend watching)?*
2. *How many of these movies can fit into a user’s allotted movie-watching time?*
3. *Is there a correlation between a movie’s popularity and the vote (or rating) awarded to it by viewers?*
4. *How do the popularity and the average score for a user’s chosen movie compare to that of alternative matching movies and the overall average for its genre? (In the case of only one movie being chosen)*
5. *How do the average popularity and the average score for a user’s chosen set of movies compare to these statistics for alternative sets of movies? (In the case of multiple movies being chosen)*

## Visualisation Design

### 1. Results (Bubble Chart)

Upon confirming their preferences, users will be navigated to a screen displaying a list of movies that correspond to these and a data visualisation providing further insight into the statistics for each of these movies (namely their popularity, the average vote awarded to them by viewers and their adherence to the user’s genre preferences). This visualisation aims to support users in making an informed decision on what movie (or combination of movies) to watch and which ones not to watch.

![Untitled](example_bubble.png)

I suggest displaying this information in a bubble chart (similar to the one shown above) but instead with the x-axis corresponding to the movie’s average score, the y-axis corresponding to the movie’s popularity and the bubble size corresponding to genre preference adherence (a standardised score relating to how closely the movie’s genres match the user’s genre preferences). The bubbles themselves won’t display any directly identifying characteristics of the movies aside from the number corresponding to its position in the list of results, so as not to overwhelm the visualisation. However, upon hovering over each bubble, more information will be displayed, such as the movie’s title, its cover image, tagline and specific statistics. 

See below a sketch displaying my envisioned design of the movie results bubble chart.

{insert design}

The questions this visualisation intends to answer are:

1. *What are the most popular/highest scoring movies that match a user’s given preferences (their preferred genres and/or the maximum length of time they have to spend watching)?*
2. *How many of these movies can fit into a user’s allotted movie-watching time?*
3. *Is there a correlation between a movie’s popularity and the vote (or rating) awarded to it by viewers?*

The advantage of using a bubble chart over other types of data visualisation is its ability to consolidate multiple (up to four) dimensions of data in a visual format, thus facilitating interpretation beyond what is achievable by most other visualisations. Given our target demographic consists of young adults who use streaming platforms and our overarching aim is to reduce “decision fatigue”, it emerges as not only appropriate, but necessary to choose a visualisation which makes it easy for users to compare a large amount of data without having to give it much thought.

### 2. User Selection Statistics (Wind Rose/Stacked Polar Bar Chart)

Finally, on confirming their selection of movie/s, users are navigated to a page displaying the same movie information shown upon hovering over the bubble chart, such as the title/s and cover image/s and, additionally, a brief description of the/each movie and a data visualisation providing a clearer gauge on how their selection compares to other options. The purpose of this visualisation is to guide users’ decision-making further, by showing a more “zoomed-in” view of the data for a small number of movies/movie combinations, whilst highlighting the user’s selected movie/s to support comparison across these options and, subsequently, facilitate the validation of their final, confirmed choice.

![Untitled](example_polar.png)

I suggest visualising this as a stacked polar bar chart (similar to the one shown above),  featuring a clearly highlighted bar corresponding to the user’s selection/s, a bar corresponding to the data average for all the movies matching the user’s preferences and the remaining bars corresponding to up to three alternative recommended movies (or sets of movies) matching the user’s preferences. The stacked segments should correspond to the movies’ popularity, average vote awarded and genre-adherence and each of these parameters can be deselected to remove them from being viewed in the visualisation. 

The questions this visualisation intends to answer are:

1. *How do the popularity and the average score for a user’s chosen movie compare to that of alternative matching movies and the overall average for its genre? (In the case of only one movie being chosen)*
2. *How do the average popularity and the average score for a user’s chosen set of movies compare to these statistics for alternative sets of movies? (In the case of multiple movies being chosen)*

The use of a stacked polar bar chart combines the key advantages of stacked bar charts (being able to easily compare different dimensions of data, as well as the aggregation of these, for a number of different variables) and that of polar bar charts (the visual benefits, such as being able to more easily distinguish slight differences in bar lengths). Again, simple and effective data visualisations are essential if this app intends to make a significant impact to the “decision fatigue” experienced by our target demographic, a consumer group often distinguished by their notably short attention spans. 

### Visual Styles

Both data visualisations, as well as the entire app, will feature styling consistent with that of Netflix, to maintain uniformity and visual association with the popular streaming platform.

### Visualisation Evaluation

1. Results (Bubble Chart)

... goes a step further by giving the option to deselect (declutter) the chart as users narrow down their decisions