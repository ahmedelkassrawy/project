FROM python:3.10-slim

#set Docker work directory
WORKDIR /code

#copy from the build context directory to the docker
COPY requirements.txt /code

#Install the python libraries
RUN pip install --no-cache-dir --upgrade -r requirements.txt

#Copy the code files and database from the build context directory to the docker
COPY *.py /code/
COPY *.db /code/

CMD ["uvicorn", "main:app","--host","0.0.0.0","--port","8080","--reload"]