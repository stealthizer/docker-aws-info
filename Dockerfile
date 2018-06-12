FROM alpine:latest
MAINTAINER Jordi Franco "stealthizer@gmail.com"
RUN apk add --update \
              python3 py-psutil \
  && pip3 install --upgrade pip \
  && rm /var/cache/apk/*

# make some useful symlinks that are expected to exist
RUN cd /usr/bin \
  && ln -sf easy_install-3.5 easy_install
ADD /app /app
WORKDIR /app
RUN pip3 install -r /app/requirements.txt
ENTRYPOINT ["python3"]
CMD ["app.py"]
