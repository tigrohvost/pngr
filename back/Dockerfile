# start by pulling the python image
#FROM python:3.8-alpine
FROM python:3.11-slim

ENV PATH="/scripts:${PATH}"
ENV PATH /usr/local/bin:$PATH

#fix ping capability issue
RUN apk update && apk upgrade
RUN apk add --no-cache libcap libcap-utils
RUN setcap cap_net_raw+ep $(which python)

# copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt

# switch working directory
WORKDIR /app

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# copy every content from the local file to the image
COPY . /app

# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]

CMD ["back.py" ]
