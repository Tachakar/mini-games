## About

Since i've finished some Django courses i wanted to build simple web app. Right now it contaitn only worlde and it's working, but in the future i plan to add some more games like tictactoe, etc. 

**Important**: This app is still under construction, some things might not work.
## Instalation

- Run: `git clone https://github.com/Tachakar/mini-games`
- Create .venv: `python3 -m venv .venv`; source it: `source .venv/bin/activate`
- Run `pip install -r requirementes.txt`
- Create superuser by running: `python3 manage.py createsuperuser`
- Create postgresql database and grant all privilages to your user
- Generate Django Secret Key([link](https://django-secret-key-generator.netlify.app/))
- Make .env and pass SECRET_KEY, DB_USER, DB_PASSWORD into it
- Run `python3 manage.py dbimportwords` for wordle to work and `npm run build` to compile .ts files
