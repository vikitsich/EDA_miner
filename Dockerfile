# our base image
FROM continuumio/anaconda3


# install Python modules needed by the Python app
COPY requirements.txt /usr/src/app/
RUN pip install -r /usr/src/app/requirements.txt

# copy files required for the app to run
COPY app.py /usr/src/app/
COPY server.py /usr/src/app/
COPY utils.py /usr/src/app/
COPY menus.py /usr/src/app/
COPY __init__.py /usr/src/app/
COPY y2d.png /
COPY apps /usr/src/app/apps
COPY assets /usr/src/app/assets

# tell the port number the container should expose
EXPOSE 5000

# run the application
CMD ["python", "/usr/src/app/app.py"]
