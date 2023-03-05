# docker build -t 192.168.43.7:30501/kafka-connector . 
# docker push 192.168.43.7:30501/kafka-connector
FROM denoland/deno:1.31.1
RUN mkdir /app
RUN mkdir -p /etc/kafkac
WORKDIR /app
COPY deno.* *.ts ./
RUN deno cache --lock=deno.lock main.ts
ENTRYPOINT ["deno", "run", "--allow-env", "--allow-net", "--allow-read", "-q", "main.ts"]
