# Streamlit on a Hugging Face Docker Space.
# HF retired the native `streamlit` SDK, so the Streamlit app ships in a
# container and serves on 7860, the port Spaces expects.
FROM python:3.11-slim

# Spaces run the container as uid 1000; give Streamlit a writable home.
RUN useradd -m -u 1000 user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false \
    STREAMLIT_SERVER_FILE_WATCHER_TYPE=none

WORKDIR $HOME/app

COPY --chown=user requirements.txt .
USER user
RUN pip install --no-cache-dir --user -r requirements.txt

COPY --chown=user app.py .
COPY --chown=user data ./data

EXPOSE 7860
CMD ["streamlit", "run", "app.py", \
     "--server.port=7860", "--server.address=0.0.0.0", "--server.headless=true"]
