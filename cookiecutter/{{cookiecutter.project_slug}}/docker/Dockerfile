# syntax=docker/dockerfile:1
FROM python:3.12.3 as builder
WORKDIR /code

RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"
RUN pip install --no-cache-dir build==1.1.1
COPY requirements.txt .
RUN --mount=type=secret,id=netrc,target=/root/.netrc \
    --mount=type=secret,id=pipconf,target=/root/.config/pip/pip.conf \
    pip install -r requirements.txt --no-cache-dir

COPY pyproject.toml .
COPY src/ ./src
RUN python -m build -w -o /dist && \
    pip install --no-cache-dir /dist/*.whl


FROM python:3.12.3-slim
EXPOSE 3000
ENV PATH="/venv/bin:$PATH"
COPY --from=builder /venv /venv

CMD ["gunicorn", "-b", "0.0.0.0:3000", "--timeout", "999", "--threads", "24", "-k", "uvicorn.workers.UvicornWorker", "app.main:server"]
