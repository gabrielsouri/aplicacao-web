FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000

# Auto-fix DS002: Run as non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser
USER appuser

# Auto-fix DS026: Health check
HEALTHCHECK --interval=30s --timeout=3s CMD curl -f http://localhost:5000/health || exit 1

CMD ["python", "app.py"]
