# Instagram Giveaway Picker Tool

This program takes some inputs from a config file and starts analysing an instagram post to pick winner(s) from comments who are qualified based on the following conditions:
  - The candidate has to tag minimum 5 persons in the comment section of a specified post.
  - The candidate has to press the like button of the post.
  - The candidate must have followed the Instagram page of the owner.

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

### Parameters

The following parameters can be or must be defined and replaced in `config.py` file.
  - `username`: If login with an Instagram account is required for some actions such as listing the followers of a user, you should define here.
    - As the default, this parameter will be used. If you want to be anonymous, you should remove this argument for the function `login_insta` in the main function.
  - `password`: This option disabled by default, and the program ask for the password interactively in the terminal. If you defined it here and also in the argument of the function `login_insta`, you save it, and do not need to enter it anymore.
  - `profile_name`: This option specifies the nae of the target profile from which the list of followers are fetched."
  - `post_id`: The ID of the target post in which the likes and comments will be processed.
  - `min_tags`: Defines the condition of how many people should be minimum tagged in the comments by a specific user to be qualified for the giveaway.
  - `tz_country`: The name of the target country of the giveaway. It is used to define the deadline based on the timezone of that country.
    - The country name must be already defined in the directory `tz_dict`
  - `total_winner`: The number of winners among qualified candidates who passed all the giveaway requirements.
  - `deadline_dict`: The deadline of the giveaway participation is defined in this dictionary type.
  - `tz_dict`: The available timezone options that can be used for `tz_country`. If another timezone is needed, it should be first defined here, and then as the `tz_country`.
    - List of the timezones can be found [here](https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568).

## Demo

![](demo.gif)

## Licence

This project is licensed under the GNU GPLv3 License - see the [LICENSE](LICENSE) file for details.

## Support

This service was originally provided for YegaNedia's services and giveaways. You can find more information on www.yeganedia.com.

If you like this project and want to support YegaNedia, you can follow the page in Instagram and subscribe in YouTube channel via the following addresses:
- Instagram Page: https://www.instagram.com/yeganedia
- YouTube Channel: https://www.youtube.com/yeganedia
