# LICENSE CDDL 1.0 + GPL 2.0
#
# --------------------------
# This is the Dockerfile for OCSG PTE 6.0
#
# REQUIRED FILES TO BUILD THIS IMAGE
# ----------------------------------
# (1) ocsg_pte_generic.jar
#     Download the Generic installer from https://edelivery.oracle.com/osdc/faces/Home.jspx
#
# (2) jdk-7u80-linux-x64.rpm
#     Download from http://www.oracle.com/technetwork/java/javase/downloads/java-archive-downloads-javase7-521261.html
#
# HOW TO BUILD THIS IMAGE
# -----------------------
# Put all downloaded files in the same directory as this Dockerfile
# Run:
#      $ sudo docker build -t netapps/ocsgpte:6.0 .
#
# Pull base image
# ---------------
FROM oraclelinux:6.6

# Maintainer
# ----------
MAINTAINER Anton R. Yuste <ayuste@optaresolutions.com>

# Environment variables required for this build
# -------------------------------------------------------------
ENV JAVA_RPM jdk-7u80-linux-x64.rpm
ENV OCSG_PKG ocsg_pte_generic.jar
ENV JAVA_HOME /usr/java/default
ENV CONFIG_JVM_ARGS -Djava.security.egd=file:/dev/./urandom
ENV JAVA_OPTIONS -Djava.security.egd=file:/dev/./urandom
ENV VNC_PORT 5900

RUN yum -y install twm Xvfb libXtst.x86_64 libXrender.x86_64 libX11.so.6 libXext.so.6 libXfixes.so.3 libXinerama.so.1 libXrandr.so.2 libXtst.so.6 libavahi-client.so.3 libavahi-common.so.3 libcrypto.so.6 libjpeg.so.62 libssl.so.6 libz.so.1 && \
    curl -O -L http://dag.wieers.com/rpm/packages/x11vnc/x11vnc-0.9.3-1.el5.rf.i386.rpm && \
    rpm -ivh x11vnc-0.9.3-1.el5.rf.i386.rpm && \
    yum clean all

# Change root password TODO: eliminate this, only for debug
RUN echo -e "welcome1\nwelcome1" | (passwd --stdin root)

# Setup required packages (unzip), filesystem, and oracle user
# ------------------------------------------------------------
RUN mkdir /u01 && \
    chmod a+xr /u01 && \
    useradd -b /u01 -m -s /bin/bash oracle

# Copy packages
COPY $OCSG_PKG /u01/
COPY $JAVA_RPM /u01/
COPY installpte.file /u01/
COPY startPTE.sh /u01/
COPY oraInst.loc /u01/

# Install and configure Oracle JDK 7u80
# -------------------------------------
RUN rpm -i /u01/$JAVA_RPM && \
    rm /u01/$JAVA_RPM

# Adjust file permissions, go to /u01 as user 'oracle' to proceed with OCSG installation
RUN chown -R oracle:oracle /u01
WORKDIR /u01
USER oracle

# Installation of OCSG
RUN mkdir -p /u01/oracle/.inventory
RUN java -jar $OCSG_PKG -ignoreSysPrereqs -novalidation -silent -responseFile /u01/installpte.file -invPtrLoc /u01/oraInst.loc -jreLoc $JAVA_HOME

# Configuration of WLS Domain
WORKDIR /u01/oracle/ocsg-pte

# Delete files
RUN rm -f /u01/$OCSG_PKG /u01/oraInst.loc /u01/installpte.file

# Expose VNC Port
EXPOSE $VNC_PORT

# Some problems with IPv6
ENV JAVA_OPTIONS $JAVA_OPTIONS -Djava.net.preferIPv4Stack=true

# Define default command to start bash.
CMD ["/u01/startPTE.sh"]
