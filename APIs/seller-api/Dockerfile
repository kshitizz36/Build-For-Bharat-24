FROM openjdk:17
ARG JAR_FILE=target/*.jar
COPY ${JAR_FILE} app.jar
ENV JAVA_OPTS="-Xmx2g"
ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -jar /app.jar"]
