# Code Cafe App
<img src="https://66.media.tumblr.com/b4597888f3b34bd1f53c1f68a6587b94/0b795c1705c90200-55/s1280x1920/5247dec10643bdf5e1c5b9ba2046bb1743be86d3.png"  width="250" height="350"  align="right">

An app with a menu enabling students to order drinks. Displays graphics representing the ratios of ingredients for each drinks, allows public users to view drink names, allows **baristas** to see recipe information, and allows shop managers to create new drinks and edit existing drinks. Uses <a href="">Auth0</a> to authenticate and log users. 



## Tasks

There are `@TODO` comments throughout the project. We recommend tackling the sections in order. Start by reading the READMEs in:

1. [`./backend/`](./backend/README.md)
2. [`./frontend/`](./frontend/README.md)

### Backend

The `./backend` directory contains a partially completed Flask server with a pre-written SQLAlchemy module to simplify your data needs. You will need to complete the required endpoints, configure, and integrate Auth0 for authentication.

[View the README.md within ./backend for more details.](./backend/README.md)

### Frontend

The `./frontend` directory contains a complete Ionic frontend to consume the data from the Flask server. You will only need to update the environment variables found within (./frontend/src/environment/environment.ts) to reflect the Auth0 configuration details set up for the backend app. 

[View the README.md within ./frontend for more details.](./frontend/README.md)

## Credits 
Logo for authentication page comes from <a href="https://www.tailorbrands.com">Tailor Brands</a>. 
