# Base image
FROM python:3.11-slim

# Working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install PyTorch CPU-only
RUN pip install --no-cache-dir --timeout=300 \
    torch==2.0.1+cpu \
    --index-url https://download.pytorch.org/whl/cpu

# Install remaining dependencies
RUN pip install --no-cache-dir --timeout=300 \
    pandas \
    numpy \
    matplotlib \
    scikit-learn \
    streamlit \
    plotly \
    seaborn

# Copy project
COPY . .

# Expose port
EXPOSE 8501

# Run dashboard
CMD ["streamlit", "run", "dashboard/app.py", \
     "--server.address=0.0.0.0", \
     "--server.port=8501"]