# Tweets
Maths Tweet with Python

Maths Tweet with mostly Python and a bit of Inkscape or Geogebra.

Some elements are provided below. More images and animations can be found in the associated directory. 

## [Hitomezashi](https://github.com/josephsalmon/Tweets/tree/master/Hitomezashi/README.md)

Hitomezashis are (numerical) decorative reinforcement stitching inspired by Japanese tradition.

[<img src="https://raw.github.com/josephsalmon/Tweets/master/Hitomezashi/svg/hitomezashi_mirror_cmap_viridis_pi_150_nq30.svg?sanitize=true" height="200">](https://github.com/josephsalmon/Tweets/tree/master/Hitomezashi/README.md)


## [Spline-ish](https://github.com/josephsalmon/Tweets/tree/master/Spline-ish/README.md)

In this part, simple iterations creating perspective function are investigated. They are prototype of [Bézier curves](https://en.wikipedia.org/wiki/B%C3%A9zier_curve), simply used for the fun.

[<img src="https://raw.github.com/josephsalmon/Tweets/master/Spline-ish/my_art/a_la_harris_007.svg?sanitize=true" height="200">](https://github.com/josephsalmon/Tweets/tree/master/Spline-ish/README.md)


##  [IslamicArt](https://github.com/josephsalmon/Tweets/tree/master/IslamicArt/README.md)

Here, simple traditional geometric constructions from the Islamic world are investigated (stars, zellige, etc.):

[<img src="https://raw.github.com/josephsalmon/Tweets/master/IslamicArt/svg/ten_star_color_e.svg?sanitize=true" height="200">](https://github.com/josephsalmon/Tweets/tree/master/IslamicArt/README.md)
[<img src="https://raw.github.com/josephsalmon/Tweets/master/IslamicArt/svg/zellige.svg?sanitize=true" height="200">](https://github.com/josephsalmon/Tweets/tree/master/IslamicArt/README.md)
[<img src="https://raw.github.com/josephsalmon/Tweets/master/IslamicArt/svg/zellige_color.svg?sanitize=true" height="200">](https://github.com/josephsalmon/Tweets/tree/master/IslamicArt/README.md)
[<img src="https://raw.github.com/josephsalmon/Tweets/master/IslamicArt/svg/Lotfallah_colored.svg?sanitize=true" height="200">](https://github.com/josephsalmon/Tweets/tree/master/IslamicArt/README.md)
[<img src="https://raw.github.com/josephsalmon/Tweets/master/IslamicArt/svg/Lotfallah_nb.svg?sanitize=true" height="200">](https://github.com/josephsalmon/Tweets/tree/master/IslamicArt/README.md)


## [Central Limit Theorem (CLT)](https://github.com/josephsalmon/Tweets/tree/master/CLT)

Here, we investigate visually random walks connections to the CLT:

[<img src="https://raw.github.com/josephsalmon/Tweets/master/CLT/svg/TCL_readme.svg?sanitize=true" height="200">](https://github.com/josephsalmon/Tweets/tree/master/CLT/README.md)

### Docker

You can run the programs using a Docker container. In this example just replace the paths according to your setup :

```bash
    sudo docker image build -t math_tweet_with_python .
    sudo docker container run -it --rm -v FULL_PATH_FOR_THE_OUTPUT:/gifs -v FULL_PATH_FOR_THIS_REPO:/code math_tweet_with_python python3 /code/Berhu_video/Beru_from_mathurin.py
    sudo docker container run -it --rm -v FULL_PATH_FOR_THE_OUTPUT:/pdf -v FULL_PATH_FOR_THE_OUTPUT:/svg -v FULL_PATH_FOR_THE_OUTPUT:/png -v FULL_PATH_FOR_THIS_REPO:/code math_tweet_with_python python3 /code/IslamicArt/ten_star.py
```
