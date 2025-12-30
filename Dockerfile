FROM python:3.13
ARG TARGETPLATFORM
WORKDIR /usr/local/app

# Install the application dependencies
COPY requirements.txt ./
RUN apt update && apt install -y firefox-esr
RUN pip install --no-cache-dir -r requirements.txt
RUN case ${TARGETPLATFORM} in \
         "linux/arm64")  GECKO_ARCH=linux-aarch64  ;; \
         "linux/aarch64")  GECKO_ARCH=linux-aarch64  ;; \
         *)    GECKO_ARCH=linux64   ;; \
    esac \
 && echo ${GECKO_ARCH} \
 && wget -q https://github.com/mozilla/geckodriver/releases/download/v0.36.0/geckodriver-v0.36.0-${GECKO_ARCH}.tar.gz -O geckodriver.tar.gz \
 && tar -xzvf geckodriver.tar.gz -C /usr/local/bin

# Copy in the source code
COPY src ./src

CMD ["python", "src/dailydriverpin.py"]
