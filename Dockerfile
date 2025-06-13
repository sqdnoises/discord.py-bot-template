FROM --platform=linux/amd64 python:3.13-slim

# Prevents python from writing .pyc files to disc (improves performance slightly in containers)
ENV PYTHONDONTWRITEBYTECODE 1

# Prevents python from buffering stdout/stderr (important for Docker logging)
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN pip install --no-cache-dir uv

# Install project dependencies
WORKDIR /bot
COPY requirements.txt .
RUN uv pip install --no-cache-dir --system -r requirements.txt

# Generate Prisma client
COPY prisma/ ./prisma/
RUN prisma generate

# Copy the source code in last to optimize rebuilding the image
COPY . .

CMD ["python", "-m", "src"]
