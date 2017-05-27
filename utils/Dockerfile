FROM civisanalytics/datascience-python
COPY process.py /src/
# VOLUME /data
RUN pip install pymongo \
&& pip install qiniu \
&& pip install requests
#ENTRYPOINT ["python","/src/process.py"]
#CMD /bin/bash


