# Calvin and Hobbes Quote Emailer

This is a simple Python application that emails you a random Calvin and Hobbes quote each day.

## Usage

To use this application, you'll need to set up a `.env` file with your email address and email password. You'll also need to fill in the `config.json` file with your email server information.

Once you have the necessary credentials set up, you can run the `main.py` file to send yourself a random quote. You can set up a scheduled task or cron job to run this script each day.

## Dependencies

This application requires the `pymongo` and `pymongo[srv]` modules to connect to a MongoDB database. You'll also need the `dotenv` and `pymongo` modules to load your email credentials.

## Acknowledgements

Thanks to Bill Watterson for creating Calvin and Hobbes, and thanks to OpenAI for creating GPT-3, which was used to generate some of the quotes in the database.

![Calvin and Hobbes](media/LetsGoExploring.jpg)
