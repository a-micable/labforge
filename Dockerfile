FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt pyproject.toml README.md ./
COPY repairloop ./repairloop
COPY tasks ./tasks
COPY oracles ./oracles
COPY app.py ./

RUN pip install --no-cache-dir -r requirements.txt \
 && pip install --no-cache-dir -e .

ENV REPAIRLOOP_RUNS_DIR=/app/runs
EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]
