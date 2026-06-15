package com.amazon.rematch.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import software.amazon.awssdk.auth.credentials.AwsBasicCredentials;
import software.amazon.awssdk.auth.credentials.AnonymousCredentialsProvider;
import software.amazon.awssdk.auth.credentials.StaticCredentialsProvider;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.bedrockruntime.BedrockRuntimeClient;

@Configuration
public class BedrockConfig {

    @Value("${aws.region:us-east-1}")
    private String region;

    @Value("${aws.accessKeyId:PLACEHOLDER}")
    private String accessKeyId;

    @Value("${aws.secretAccessKey:PLACEHOLDER}")
    private String secretAccessKey;

    @Bean
    public BedrockRuntimeClient bedrockRuntimeClient() {
        boolean hasRealCredentials =
            accessKeyId != null  && !accessKeyId.equals("PLACEHOLDER")  && !accessKeyId.isBlank() &&
            secretAccessKey != null && !secretAccessKey.equals("PLACEHOLDER") && !secretAccessKey.isBlank();

        if (hasRealCredentials) {
            return BedrockRuntimeClient.builder()
                .region(Region.of(region))
                .credentialsProvider(StaticCredentialsProvider.create(
                    AwsBasicCredentials.create(accessKeyId, secretAccessKey)
                ))
                .build();
        }

        // No real credentials — build a no-op client. BedrockService already has a
        // try/catch that returns the fallback text whenever the API call fails.
        return BedrockRuntimeClient.builder()
            .region(Region.of(region))
            .credentialsProvider(AnonymousCredentialsProvider.create())
            .build();
    }
}
