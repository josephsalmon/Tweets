# Sismograph and sinus

Here I provide some code to solve the last exam question of my course HLMA310.
This is inspired and adapted from reading (https://1ucasvb.tumblr.com/post/42906053623/in-a-previous-post-i-showed-how-to-geometrically).

<img src="sismograph_sinus.gif" width="500">

The code is in Python: [sismograph_sinus.py](sismograph_sinus.py) and produces an mp4 image ([sismograph_sinus.mp4](sismograph_sinus.mp4)) , and a gif could also be obtained with ffmpeg ([sismograph_sinus.gif](sismograph_sinus.gif)). 

Note: the convertion to gif can be done following:

https://dev.to/halivert/convert-mp4-to-gif-3idd

```
ffmpeg -i sismograph_sinus.mp4 -vf fps=5 frames/%03d.png

convert frames/* output.gif

```

