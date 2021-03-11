# Builds the auDeep docker image to use old TensorFlow 1.x.
FROM tensorflow/tensorflow:1.15.5-gpu

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y \
        --no-install-recommends libsndfile1 python3.7 \
    && apt-get autoremove

RUN ln -sf python3.7 /usr/bin/python3 \
    && python3 -m pip install -U pip setuptools

WORKDIR /home/audeep
COPY setup.py DESCRIPTION.md /home/audeep/
COPY audeep /home/audeep/audeep
RUN python3 setup.py install \
    && rm -rf /home/audeep
# To keep matplotlib happy
RUN mkdir -p -m 777 /.{cache,config}/matplotlib

WORKDIR /work
CMD [ "/bin/bash" ]
