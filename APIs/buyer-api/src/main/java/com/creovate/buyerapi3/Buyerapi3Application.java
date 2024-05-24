package com.creovate.buyerapi3;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.hbase.HBaseConfiguration;
import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.Connection;
import org.apache.hadoop.hbase.client.ConnectionFactory;
import org.apache.hadoop.hbase.client.Get;
import org.apache.hadoop.hbase.client.Result;
import org.apache.hadoop.hbase.client.Table;
import org.apache.hadoop.hbase.util.Bytes;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.scheduling.annotation.Async;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.util.UriComponentsBuilder;

import java.net.URI;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.Executor;
import java.util.stream.Collectors;

@SpringBootApplication
@EnableAsync
public class Buyerapi3Application {

    static final String hbaseIP = "10.190.0.4";

    public static void main(String[] args) {
        SpringApplication.run(Buyerapi3Application.class, args);
    }

    @Bean(name = "taskExecutor")
    public Executor taskExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(10);
        executor.setMaxPoolSize(50);
        executor.setQueueCapacity(100);
        executor.setThreadNamePrefix("HBaseLookup-");
        executor.initialize();
        return executor;
    }

    @Async("taskExecutor")
    public CompletableFuture<String> hbaseConn(String pin) {
        Configuration config = HBaseConfiguration.create();
        config.set("hbase.zookeeper.quorum", hbaseIP);
        config.set("hbase.zookeeper.property.clientPort", "2181");

        try (Connection connection = ConnectionFactory.createConnection(config);
             Table table = connection.getTable(TableName.valueOf("pincode_serviceability"))) {

            Get get = new Get(Bytes.toBytes(pin));
            Result result = table.get(get);
            byte[] value = result.getValue(Bytes.toBytes("cf"), Bytes.toBytes("merchant_id"));

            if (value != null) {
                String merchants = Bytes.toString(value);
                logger(" " + pin + "  -> " + merchants);
                return CompletableFuture.completedFuture(merchants);
            } else {
                logger("NO MERCHANTS FOUND FOR " + pin);
                return CompletableFuture.completedFuture("Null");
            }

        } catch (Exception e) {
            e.printStackTrace();
            return CompletableFuture.completedFuture("Error: " + e.getMessage());
        }
    }

    public static void logger(String txt) {
        System.out.println("########################################");
        System.out.println();
        System.out.println();
        System.out.println("            " + txt + "                   ");
        System.out.println();
        System.out.println();
        System.out.println("########################################");
    }

    @RestController
    public class HBaseController {

        private final Buyerapi3Application application;

        public HBaseController(Buyerapi3Application application) {
            this.application = application;
        }

        @GetMapping("/download")
        public CompletableFuture<String> getMerchants(@RequestParam String data, @RequestParam String mode) {
            logger("GET REQUEST FOR " + data + " with mode " + mode);

            // Split the input data by comma and process based on mode
            List<String> processedPincodes = new ArrayList<>();
            String[] inputs = data.split(",");

            switch (mode) {
                case "pincodes":
                    // Assume data is a list of pincodes
                    for (String pincode : inputs) {
                        processedPincodes.add(pincode.trim());
                    }
                    break;

                case "gps":
                    // Assume data is a list of latitude and longitude pairs
                    for (int i = 0; i < inputs.length; i += 2) {
                        String latitude = inputs[i].trim();
                        String longitude = inputs[i + 1].trim();
                        // Convert GPS coordinates to pincode
                        List<String> pincodes = getPincodeFromCoordinates(latitude, longitude);
                        if (pincodes != null) {
                            processedPincodes.addAll(pincodes);
                        }
                    }
                    break;

                case "location":
                    // Assume data is a list of location names
                    for (String location : inputs) {
                        // Convert location name to pincodes
                        List<String> pincodes = getPincodesFromLocation(location.trim());
                        processedPincodes.addAll(pincodes);
                    }
                    break;

                default:
                    return CompletableFuture.completedFuture("Invalid mode specified");
            }


            List<CompletableFuture<String>> futures = processedPincodes.stream()
                .map(application::hbaseConn)
                .collect(Collectors.toList());

            // Combine results of all futures
            CompletableFuture<Void> allOf = CompletableFuture.allOf(futures.toArray(new CompletableFuture[0]));
            return allOf.thenApply(v -> futures.stream()
                .map(CompletableFuture::join)
                .collect(Collectors.joining(", ")));
        }

        private List<String> getPincodeFromCoordinates(String latitude, String longitude) {
            List<String> pinList = new ArrayList<>();
            String baseUrl = "https://nominatim.openstreetmap.org/reverse";
            URI uri = UriComponentsBuilder.fromHttpUrl(baseUrl)
                    .queryParam("format", "json")
                    .queryParam("lat", latitude)
                    .queryParam("lon", longitude)
                    .build()
                    .toUri();

            RestTemplate restTemplate = new RestTemplate();
            try {
                Map<String, Object> response = restTemplate.getForObject(uri, Map.class);
                if (response != null && response.get("address") != null) {
                    Map<String, Object> address = (Map<String, Object>) response.get("address");
                    if (address.get("postcode") != null) {
                        pinList.add(address.get("postcode").toString());
                    }
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
            return pinList;
        }

        private List<String> getPincodesFromLocation(String locationName) {
            List<String> pinList = new ArrayList<>();
            String baseUrl = "https://api.postalpincode.in/postoffice/" + locationName;
            URI uri = UriComponentsBuilder.fromHttpUrl(baseUrl).build().toUri();

            RestTemplate restTemplate = new RestTemplate();
            try {
                List<Map<String, Object>> response = restTemplate.getForObject(uri, List.class);
                if (response != null && !response.isEmpty()) {
                    Map<String, Object> data = response.get(0);
                    List<Map<String, Object>> postOffices = (List<Map<String, Object>>) data.get("PostOffice");
                    for (Map<String, Object> postOffice : postOffices) {
                        pinList.add((String) postOffice.get("Pincode"));
                    }
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
            return pinList;
        }
    }
}
