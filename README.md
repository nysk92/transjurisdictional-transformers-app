# transjurisdictional-transformers-app
A tool to find semantically similar legislation across different jurisdictions, built on flask. 
An implementation of [this project](https://github.com/nysk92/transjurisdictional-transformers), where you will find further info about the goals of the project and the correct way to format your data should you wish to prepare and use your own data for this application.
This repo is already preloaded with test data for selected legislation.

## Instructions to Run
After cloning to your machine, unzip data folder before use, that has been compressed to allow upload to github.
Use `config.json` to specify the filepaths of your raw data and vectors. 
To start the app, run `./start_flask.sh` in your terminal. Open the url specified in the terminal in your browser to use the app.

When you can view the app in the browser, click on your preferred area of law. On the next page, choose between the three choice of embeddings (simple, medium, deep) and on the next page, select your input provision number (following the format in the autocomplete list).

