FROM python:3.11-slim
WORKDIR $HOME/app
COPY . .
RUN pip install -r requirements.txt
VOLUME /data
EXPOSE 21111
CMD ["python", "-m", "apis.search_api"]