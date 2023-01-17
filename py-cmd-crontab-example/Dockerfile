FROM zhugecheng/python3.10/python3.10:1.0.1

EXPOSE 8000
RUN mkdir /your-work-dir
WORKDIR /your-work-dir
COPY . /your-work-dir

#启动
RUN chmod +x ./init.sh && dos2unix ./init.sh
ENTRYPOINT ["/bin/bash","-c","./init.sh"]