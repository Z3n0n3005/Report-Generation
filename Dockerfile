FROM ubuntu

RUN apt-get update && apt-get install \
    && apt-get install openjdk-17-jdk openjdk-17-jre -y && java --version 
    # && curl -s "https://get.sdkman.io" | bash \
    # && source "$HOME/.sdkman/bin/sdkman-init.sh" \
    # && sdk install gradle 8.4 \ 
    # && gradle wrapper --gradle-version 8.4

