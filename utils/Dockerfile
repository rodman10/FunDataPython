FROM dhorta/science-conda2
COPY process.py RedisQueue.py /src/
# VOLUME /data
RUN pip install pymongo \
&& pip install redis \
&& pip install qiniu \
&& pip install requests
ENTRYPOINT ["python","/src/process.py"]
#CMD /bin/bash


