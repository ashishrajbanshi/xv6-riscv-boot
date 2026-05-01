FROM python:3.12-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends qemu-system-misc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY serverless-trigger/handler.py /app/handler.py
COPY serverless-trigger/noop_handler.py /app/noop_handler.py
COPY serverless-trigger/serve.py /app/serve.py
COPY kernel/kernel /app/xv6/kernel/kernel
COPY fs.img /app/xv6/fs.img

ENV PORT=8080
ENV XV6_ROOT=/app/xv6
ENV XV6_KERNEL=/app/xv6/kernel/kernel
ENV XV6_FS=/app/xv6/fs.img
ENV XV6_BOOT_TIMEOUT_SEC=5
ENV XV6_LOG_LIMIT=500
ENV XV6_MEMORY=128M
ENV XV6_CPUS=1

EXPOSE 8080

CMD ["python", "serve.py"]
