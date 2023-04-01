FROM jupyter/scipy-notebook:python-3.10

#VOLUME . /home/jovyan
COPY requirements.txt requirements.txt
RUN conda install --file requirements.txt