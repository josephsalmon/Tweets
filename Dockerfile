FROM debian 

RUN apt update && apt upgrade -y && \
    apt install -y bison \
		   cm-super \
		   dvipng \ 
		   flex \
		   imagemagick \
		   libcairo2-dev \
		   libtool \
 		   libxml2-dev \
                   pkg-config \
	           python3 \
		   python3-pip \
		   texlive-latex-extra \
		   zlib1g-dev

COPY requirements.txt /requirements.txt
RUN python3 -m pip install -r /requirements.txt

