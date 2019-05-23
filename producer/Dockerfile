FROM python:3.7.2 as base
WORKDIR /install
COPY requirements.txt /requirements.txt
RUN pip install --install-option="--prefix=/install" -r /requirements.txt

FROM base
COPY --from=base /install /usr/local
COPY . /app
WORKDIR /app
CMD ["python", "main.py", "london"]