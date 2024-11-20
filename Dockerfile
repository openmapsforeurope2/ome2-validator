FROM qgis/qgis:3.40.0

# Set environment variables for QGIS and python
ENV QGIS_PREFIX_PATH=/usr
ENV QT_QPA_PLATFORM=offscreen
ENV XDG_RUNTIME_DIR=/tmp/runtime-root
ENV PYTHONPATH=/usr/share/qgis/python/plugins

WORKDIR /app
COPY . /app

# Note: the file EXTERNALLY-MANAGED prevents pip3 from installing packages
RUN rm /usr/lib/python3.12/EXTERNALLY-MANAGED && \
    pip3 install -r requirements.txt
