# MPI backend

Minimal backend for the Motorcycle Part Identifier web app.

## Description

Python/Flask app that fetches motorcycle part details from eBay.

 It searches eBay for part numbers, and then attempts to build a part title from the search results by looking at common words.

## Development

### Obtaining an eBay AppID

eBay API usage requires an AppID key that is sent with each request. To obtain an API key, register for a developer account [here](https://developer.ebay.com).

### Setting the eBay AppId for this app

This app requires that your eBay AppID is set as an environment variable (```EBAY_APPID```). 

You can either set that explicitly, or place .env file in the root folder with ```EBAY_APPID = YOUR_APP_ID_HERE```.

An example .env file is included as .env.example.

### Running a local copy

To get a local copy up and running follow the steps below.

1. Clone the repo
   ```sh
   git clone https://github.com/aduda9/mpi-backend.git
   ```
2. Install python packages
   ```sh
   pip install -r requirements.txt
   ```
3. Start (see note below)
   ```sh
   flask run
   ```

### Flask notes

If you're working with the MPI frontend, you may want to run the backend over HTTPS to avoid [mixed content](https://web.dev/what-is-mixed-content/) issues.

1. Ensure pyopenssl is installed
   ```sh
   pip install pyopenssl
   ```
2. Run flask with an adhoc SSL cert
   ```sh
   flask run --cert=adhoc
   ```

See Miguel Grinberg's [post](https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https) on Flask over HTTPS for more info.

## License

MIT. See LICENSE.txt

