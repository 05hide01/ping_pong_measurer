FROM python:3
USER root

RUN apt-get update
RUN apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

RUN apt-get install -y vim less
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN apt-get install -y git

RUN python -m pip install jupyterlab
RUN python -m pip install eclipse-zenoh
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y

WORKDIR /opt
RUN git clone https://github.com/eclipse-zenoh/zenoh-python.git
RUN curl https://sh.rustup.rs -sSf | sh
RUN cd zenoh-python
RUN pip install -r requirements-dev.txt
RUN maturin build --release
RUN pip install ./target/wheels/*.whl

WORKDIR /opt
RUN git clone https://github.com/b5g-ex/ping_pong_measurer_zenoh_python.git



