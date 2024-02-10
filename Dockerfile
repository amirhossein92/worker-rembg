# Use the base image from 'repo/image'
FROM danielgatis/rembg@sha256:682b8308df6c2ed8e9496f86c9333a3a5d0e1c79b691bdd9d0c85781bf9a41f8

ADD src .

# Set permissions and specify the command to run
RUN chmod +x /start.sh
CMD /start.sh
