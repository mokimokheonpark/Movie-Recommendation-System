# Movie Recommendation System

This project implements two distinct movie recommendation systems using machine learning techniques, specifically utilizing cosine similarity to provide personalized recommendations to users.

## Features

The project has the following features:
- One system is based on cast, director, genres and keywords, and another system is based on overview(main plot points, storyline, etc.).
- The systems provide multiple recommendations, so the user can discover new movies based on their preferences.
- The systems display images and titles of the recommended movies, so the user can easily browse and select the movies they want to watch.
- The systems use the TMDb API to obtain movie data, so the recommendations are based on a large and diverse database of movies.
- The systems support user-friendly interfaces, which allow the user to select a movie and obtain recommendations with just a few clicks.

## Dependencies

This project requires the following dependencies:
- pandas: A data manipulation library used to read and analyze the CSV files containing the movie data
- numpy: A numerical computation library used to handle arrays and matrices
- sklearn: A machine learning library used to perform text feature extraction and compute cosine similarity scores
- tmdbv3api: A wrapper library used to interact with The Movie Database (TMDB) API, which is used to retrieve details about movies
- streamlit: A library used to build interactive web applications with Python

## Installation

To get started with the project, follow the steps below:
1. Clone the repository using the following command: git clone https://github.com/mokimokheonpark/Movie-Recommendation-System.git
2. Install the required libraries using the following command: pip install pandas numpy scikit-learn tmdbv3api streamlit
3. You will need a TMDb API key to access movie data through the TMDB API. Please sign up for an API key at https://www.themoviedb.org/settings/api and replace the value of tmdb.api_key in the codes (line 79 in app1.py and line 32 in app2.py) with your own API key

## Usage

To use the movie recommendation systems, follow the steps below:
1. Navigate to the project directory using the terminal.
2. To start the first recommendation system which is based on cast, director, genres and keywords, run app1.py using the following command: streamlit run app1.py&nbsp;&nbsp;&nbsp;This will open a web page in your default browser.
3. Enter the name of a movie you like in the text box provided and click on the "Get Recommendations" button. The system will display a list of 20 recommended movies based on your input.
4. To try the second recommendation system which is based on overview(main plot points, storyline, etc.), run app2.py using the following command: streamlit run app2.py&nbsp;&nbsp;&nbsp;This will open another web page.
5. Similar to the first system, enter the name of a movie you like and click on the "Get Recommendations" button to see a list of 20 recommended movies.
6. To exit the system, press Ctrl+C in the terminal to stop the streamlit server.

## Contributions

Contributions to the project are welcome! If you find any issues or have any suggestions for improvement, feel free to create an issue or a pull request.

## License

The project is licensed under the MIT License.
