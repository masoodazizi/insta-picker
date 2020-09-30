# Instagram Giveaway Picker Tool

This program takes some inputs from a config file and starts analysing an instagram post to pick winner(s) from comments who are qualified based on specific conditions.

## Getting Started

You need to first obviously clone this repository on your local machine. Then, you should change parameteres in the `config.py` file. If you have all requirements ready there, you can just simply run the Python program in your terminal.

```
$ ./insta-picker.py
```

If you have not made the Python script executable, you may use the following command:

```
$ python3 insta-picker.py
```

### Prerequisits

- This program was tested on MacOS Catalina, and should work on other MacOS versions as well as other unix-based operating systems. Since it is written in Python, I would assume Windows with Python should also be fine with it.
- Python3 is required for this script. The exact version which tested is `Python 3.8.3`
- [Instaloader](https://instaloader.github.io/) package should be installed. You can use the following pip command to install it.
```
$ pip3 install instaloader
```
- The following Python packages are required and should be available/installed:
  - pytz (might not be by default installed)
  - datetime (default package)
  - time (default package)
  - random (default package)
 
## Licence

This project is licensed under the GNU GPLv3 License - see the LICENSE.md file for details.

## Support

This service was originally provided for YegaNedia's services and giveaways. You can find more information on [www.yeganedia.com].

If you like this project and want to support YegaNedia, you can follow the page in Instagram and subscribe in YouTube channel via the following addresses:
- Instagram Page: https://www.instagram.com/yeganedia
- YouTube Channel: https://www.youtube.com/yeganedia
