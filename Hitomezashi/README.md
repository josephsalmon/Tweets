# Hitomezashi

Here I provide some code for te numerical creation of Hitomezashi art.

What is Hitomezashi? Here is an example:

<img src="my_art/hitomezashi_exp_128_blue_orange.png" width="300">

and animated ones:
<p float="left">
<img src="my_art/expRdBu150.gif"  height="300">
<img src="my_art/piRdBu150.gif" height="300">
<img src="my_art/sqrt2RdBu150.gif" width="300">
</p>
According to Wikipedia, Hitomezashi is particular form of Sashiko, a form of decorative reinforcement stitching,
see https://en.wikipedia.org/wiki/Sashiko and also
https://www.romordesigns.com/journal/2018/10/18/sashiko-the-art-of-japanese-embroidery for some sewing examples.

I became aware of this thanks to Annie Perkins Math Art Challenge:
https://twitter.com/anniek_p/status/1244220881347502080.
A nice video on the topic is provided by her at:
https://twitter.com/anniek_p/status/1244220881347502080.


The way the Python code [hitomezashi.py](hitomezashi.py) produces the images on this page is as follows: the size of the image is governed by `n_iter`, and the output will draw a `n_iter x n_iter` figure.
The sequence of 1's and 0's (of size `n_iter`) used for the generation (the "seed"), has several options (see below).
The little dash as drawn as follows:

## Column filling:
- If the i-th digit is a 1, start the i-th column by a dash, then a blank, then a dash, then etc.
- If the i-th digit is a 0, start the i-th column by a blank, then a blank, then a dash, then etc.

## Row filling:
- If the i-th digit is a 1, start the i-th row by a dash, then a blank, then a dash, then etc.
- If the i-th digit is a 0, start the i-th row by a blank, then a blank, then a dash, then etc.

The provided code proposes various "seeds", i.e.,  sequences to start the process:

- a random sequence (default)
- the parity of the fractional part of a real number (in the list  <img src="https://render.githubusercontent.com/render/math?math=\exp(1), \pi, \sqrt{2}"> etc.).



Type | Black and white             |  Colored | Symmetrized + colored
:-------------------------:|:-------------------------:|:-------------------------:|:-------------------------:
`random` | <img src="https://raw.github.com/josephsalmon/Tweets/master/Hitomezashi/svg/hitomezashi_cmap_random_150_nq015.svg?sanitize=true" width="300" > | <img src="https://raw.github.com/josephsalmon/Tweets/master/Hitomezashi/svg/hitomezashi_cmap_Blues_random_150_nq30.svg?sanitize=true" width="300" > | <img src="https://raw.github.com/josephsalmon/Tweets/master/Hitomezashi/svg/hitomezashi_mirror_cmap_Blues_random_150_nq30.svg?sanitize=true" width="300">
`exp` | <img src="https://raw.github.com/josephsalmon/Tweets/master/Hitomezashi/svg/hitomezashi_cmap_exp_150_nq015.svg?sanitize=true" width="300" >  |<img src="https://raw.github.com/josephsalmon/Tweets/master/Hitomezashi/svg/hitomezashi_cmap_RdBu_exp_150_nq30.svg?sanitize=true" width="300"> | <img src="https://raw.github.com/josephsalmon/Tweets/master/Hitomezashi/svg/hitomezashi_mirror_cmap_RdBu_exp_150_nq30.svg?sanitize=true" width="300">
`pi` | <img src="https://raw.github.com/josephsalmon/Tweets/master/Hitomezashi/svg/hitomezashi_cmap_pi_150_nq015.svg?sanitize=true" width="300" >  |<img src="https://raw.github.com/josephsalmon/Tweets/master/Hitomezashi/svg/hitomezashi_cmap_viridis_pi_150_nq30.svg?sanitize=true" width="300"> | <img src="https://raw.github.com/josephsalmon/Tweets/master/Hitomezashi/svg/hitomezashi_mirror_cmap_viridis_pi_150_nq30.svg?sanitize=true" width="300">
`sqrt2` | <img src="https://raw.github.com/josephsalmon/Tweets/master/Hitomezashi/svg/hitomezashi_cmap_sqrt2_150_nq015.svg?sanitize=true" width="300" >  |<img src="https://raw.github.com/josephsalmon/Tweets/master/Hitomezashi/svg/hitomezashi_cmap_twilight_sqrt2_150_nq30.svg?sanitize=true" width="300"> | <img src="https://raw.github.com/josephsalmon/Tweets/master/Hitomezashi/svg/hitomezashi_mirror_cmap_twilight_sqrt2_150_nq30.svg?sanitize=true" width="300">
`10101` | <img src="https://raw.github.com/josephsalmon/Tweets/master/Hitomezashi/svg/hitomezashi_cmap_101010_150_nq015.svg?sanitize=true" width="300" >  |<img src="https://raw.github.com/josephsalmon/Tweets/master/Hitomezashi/svg/hitomezashi_cmap_twilight_shifted_101010_150_nq015.svg?sanitize=true" width="300"> | <img src="https://raw.github.com/josephsalmon/Tweets/master/Hitomezashi/svg/hitomezashi_mirror_cmap_101010_150_nq015.svg?sanitize=true" width="300">

