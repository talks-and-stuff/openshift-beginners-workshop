FROM fedora
COPY app.py app.py
RUN dnf install python3-pip -y
RUN pip3 install openshift
STOPSIGNAL SIGKILL
CMD python3 -u app.py
