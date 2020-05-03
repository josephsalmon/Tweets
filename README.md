# Tweets
Maths Tweet with Python

## Docker

You can run any of the programs using a container, example:

    sudo docker image build -t math_tweet_with_python .
    sudo docker container run -it --rm -v FULL_PATH_THE_OUTPUT:/gifs -v FULL_PATH_FOR_THIS_REPO:/tweets math_tweet_with_python python3 /tweets/Berhu_video/Beru_from_mathurin.py
