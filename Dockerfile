FROM thisistheplace/gmsh:latest

# Install Python dependencies
ADD requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src /src

WORKDIR /src