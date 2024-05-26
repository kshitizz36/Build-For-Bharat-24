package com.creovate.buyerapi3;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.hbase.HBaseConfiguration;
import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.*;
import org.apache.hadoop.hbase.util.Bytes;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.scheduling.annotation.Async;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.util.UriComponentsBuilder;

import java.net.URI;
import java.util.*;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.Executor;
import java.util.stream.Collectors;

@SpringBootApplication
@EnableAsync
public class Buyerapi3Application {

    static final String hbaseIP = "10.190.0.4";
    private static Connection hbaseConnection;

    public static void main(String[] args) {
        SpringApplication.run(Buyerapi3Application.class, args);
        // Initialize HBase connection pool
        Configuration config = HBaseConfiguration.create();
        config.set("hbase.zookeeper.quorum", hbaseIP);
        config.set("hbase.zookeeper.property.clientPort", "2181");
        try {
            hbaseConnection = ConnectionFactory.createConnection(config);
        } catch (Exception e) {
            e.printStackTrace();
        }
        logger("initialized");
    }

    @Bean(name = "taskExecutor")
    public Executor taskExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(20);
        executor.setMaxPoolSize(100);
        executor.setQueueCapacity(200);
        executor.setThreadNamePrefix("HBaseLookup-");
        executor.initialize();
        return executor;
    }

    @Async("taskExecutor")
    public CompletableFuture<String> hbaseConn(String pin) {
        try (Table table = hbaseConnection.getTable(TableName.valueOf("pincode_serviceability"))) {
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

    @Async("taskExecutor")
    public CompletableFuture<List<String>> scanPincodes() {
        List<String> pincodes = new ArrayList<>();
        try (Table table = hbaseConnection.getTable(TableName.valueOf("pincode_serviceability"))) {
            Scan scan = new Scan();
            scan.setCaching(1000);
            try (ResultScanner scanner = table.getScanner(scan)) {
                for (Result result : scanner) {
                    pincodes.add(Bytes.toString(result.getRow()));
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return CompletableFuture.completedFuture(pincodes);
    }

    @Async("taskExecutor")
    public CompletableFuture<List<String>> scanPincodesForMerchant(String merchant) {
        List<String> pincodes = new ArrayList<>();
        try (Table table = hbaseConnection.getTable(TableName.valueOf("pincode_serviceability"))) {
            Scan scan = new Scan();
            scan.addColumn(Bytes.toBytes("cf"), Bytes.toBytes("merchant_id"));
            try (ResultScanner scanner = table.getScanner(scan)) {
                for (Result result : scanner) {
                    byte[] value = result.getValue(Bytes.toBytes("cf"), Bytes.toBytes("merchant_id"));
                    if (value != null) {
                        String merchants = Bytes.toString(value);
                        if (Arrays.asList(merchants.split(",")).contains(merchant)) {
                            pincodes.add(Bytes.toString(result.getRow()));
                        }
                    }
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return CompletableFuture.completedFuture(pincodes);
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
        private final Map<String, String> localCache = new HashMap<>();
        private final RestTemplate restTemplate = new RestTemplate();

        public HBaseController(Buyerapi3Application application) {
            this.application = application;
        }

        @GetMapping("/download")
        public CompletableFuture<String> getMerchants(@RequestParam String data, @RequestParam String mode) {
            logger("GET REQUEST FOR " + data + " with mode " + mode);

            List<String> processedPincodes = processInputData(data, mode);
            if (processedPincodes == null) {
                return CompletableFuture.completedFuture("Invalid mode specified");
            }

            List<CompletableFuture<String>> futures = processedPincodes.parallelStream()
                    .map(pin -> localCache.containsKey(pin) ? CompletableFuture.completedFuture(localCache.get(pin)) : application.hbaseConn(pin))
                    .collect(Collectors.toList());

            CompletableFuture<Void> allOf = CompletableFuture.allOf(futures.toArray(new CompletableFuture[0]));
            return allOf.thenApply(v -> {
                List<String> results = futures.stream()
                        .map(CompletableFuture::join)
                        .collect(Collectors.toList());
                cacheResults(processedPincodes, results);
                return String.join(", ", results);
            });

        }

        @GetMapping("/download/allpincodes")
        public CompletableFuture<List<String>> getAllPincodes() {
            return application.scanPincodes().thenApply(pincodes -> {
                pincodes.forEach(pin -> logger("Pincode: " + pin));
                return pincodes;
            });
        }

        @GetMapping("/download/merchants")
        public CompletableFuture<String> getPincodesByMerchant(@RequestParam String merchant, @RequestParam(required = false) String pin) {
            if (pin != null && !pin.isEmpty()) {
                return application.hbaseConn(pin).thenApply(result -> {
                    if (result != null && !result.equals("Null")) {
                        return result;
                    } else {
                        return "Merchant not found for pincode: " + pin;
                    }
                });
            } else {
                return application.scanPincodesForMerchant(merchant).thenApply(pincodes -> {
                    if (!pincodes.isEmpty()) {
                        return "Merchant " + merchant + " services pincodes: " + String.join(", ", pincodes);
                    } else {
                        return "Merchant " + merchant + " not found";
                    }
                });
            }
        }

        private List<String> processInputData(String data, String mode) {
            List<String> processedPincodes = new ArrayList<>();
            String[] inputs = data.split(",");

            switch (mode) {
                case "pincodes":
                    processedPincodes = Arrays.stream(inputs)
                            .parallel()
                            .map(String::trim)
                            .collect(Collectors.toList());
                    break;
                case "gps":
                    List<CompletableFuture<List<String>>> futures = Arrays.stream(inputs)
                            .parallel()
                            .map(coords -> {
                                String[] coordParts = coords.trim().split(" ");
                                if (coordParts.length == 2) {
                                    return getPincodeFromCoordinates(coordParts[0], coordParts[1]);
                                } else {
                                    return CompletableFuture.completedFuture(Collections.<String>emptyList());
                                }
                            })
                            .collect(Collectors.toList());

                    CompletableFuture<Void> allOf = CompletableFuture.allOf(futures.toArray(new CompletableFuture[0]));
                    allOf.join();

                    processedPincodes = futures.stream()
                            .flatMap(future -> future.join().stream())
                            .collect(Collectors.toList());
                    break;
                case "location":
                    List<CompletableFuture<List<String>>> locationFutures = Arrays.stream(inputs)
                            .parallel()
                            .map(location -> getPincodesFromLocation(location.trim()))
                            .collect(Collectors.toList());

                    CompletableFuture<Void> allLocationFutures = CompletableFuture.allOf(locationFutures.toArray(new CompletableFuture[0]));
                    allLocationFutures.join();

                    processedPincodes = locationFutures.stream()
                            .flatMap(future -> future.join().stream())
                            .collect(Collectors.toList());
                    break;
                default:
                    return null;
            }

            return processedPincodes;
        }

        @Async("taskExecutor")
        public CompletableFuture<List<String>> getPincodeFromCoordinates(String latitude, String longitude) {
            List<String> pinList = new ArrayList<>();
            String baseUrl = "https://nominatim.openstreetmap.org/reverse";
            URI uri = UriComponentsBuilder.fromHttpUrl(baseUrl)
                    .queryParam("format", "json")
                    .queryParam("lat", latitude)
                    .queryParam("lon", longitude)
                    .build()
                    .toUri();

            try {
                ResponseEntity<Map<String, Object>> responseEntity = restTemplate.exchange(uri, HttpMethod.GET, null, new ParameterizedTypeReference<Map<String, Object>>() {});
                Map<String, Object> response = responseEntity.getBody();
                if (response != null && response.get("address") instanceof Map) {
                    @SuppressWarnings("unchecked")
                    Map<String, Object> address = (Map<String, Object>) response.get("address");
                    if (address.get("postcode") != null) {
                        pinList.add(address.get("postcode").toString());
                    }
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
            return CompletableFuture.completedFuture(pinList);
        }

        @Async("taskExecutor")
        public CompletableFuture<List<String>> getPincodesFromLocation(String locationName) {
            List<String> pinList = new ArrayList<>();
            String baseUrl = "https://api.postalpincode.in/postoffice/" + locationName;
            URI uri = UriComponentsBuilder.fromHttpUrl(baseUrl).build().toUri();

            try {
                ResponseEntity<List<Map<String, Object>>> responseEntity = restTemplate.exchange(uri, HttpMethod.GET, null, new ParameterizedTypeReference<List<Map<String, Object>>>() {});
                List<Map<String, Object>> response = responseEntity.getBody();
                if (response != null && !response.isEmpty()) {
                    Map<String, Object> data = response.get(0);
                    if (data.get("PostOffice") instanceof List) {
                        @SuppressWarnings("unchecked")
                        List<Map<String, Object>> postOffices = (List<Map<String, Object>>) data.get("PostOffice");
                        for (Map<String, Object> postOffice : postOffices) {
                            pinList.add((String) postOffice.get("Pincode"));
                        }
                    }
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
            return CompletableFuture.completedFuture(pinList);
        }

        private void cacheResults(List<String> pincodes, List<String> results) {
            for (int i = 0; i < pincodes.size(); i++) {
                localCache.put(pincodes.get(i), results.get(i));
            }
        }
    }
}
