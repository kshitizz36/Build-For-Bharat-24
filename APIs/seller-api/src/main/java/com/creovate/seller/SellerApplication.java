package com.creovate.seller;

import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVParser;
import org.apache.commons.csv.CSVRecord;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.hbase.HBaseConfiguration;
import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.*;
import org.apache.hadoop.hbase.util.Bytes;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.core.task.TaskExecutor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.scheduling.annotation.Async;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.Reader;
import java.util.*;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ConcurrentHashMap;
import java.util.logging.Logger;

@RestController
@SpringBootApplication
public class SellerApplication {

    public final static String hbaseIP = "10.190.0.4";

    private static final Logger logger = Logger.getLogger(SellerApplication.class.getName());
    private final TaskExecutor taskExecutor;
    private final Configuration hbaseConfig;
    private final Map<String, String> processingStatus = new ConcurrentHashMap<>();
    private final Map<String, List<Map<String, List<String>>>> parsedDataMap = new ConcurrentHashMap<>();
    int setcnt = 0;

    public SellerApplication(TaskExecutor taskExecutor) {
        this.taskExecutor = taskExecutor;
        this.hbaseConfig = HBaseConfiguration.create();
        this.hbaseConfig.set("hbase.zookeeper.quorum", hbaseIP);
        this.hbaseConfig.set("hbase.zookeeper.property.clientPort", "2181");
    }

    public static void main(String[] args) {
        SpringApplication.run(SellerApplication.class, args);
    }

    @PostMapping(value = "/upload/csv")
    public ResponseEntity<Map<String, Object>> readFile(@RequestPart MultipartFile file) {
        String processingId = UUID.randomUUID().toString();
        processingStatus.put(processingId, "Processing started");
        try {
            CompletableFuture.runAsync(() -> parseAndSendCSV(file, processingId), taskExecutor);
            loggerx("Parsing has started");
            Map<String, Object> response = new HashMap<>();
            response.put("message", "File processing started with ID: " + processingId);
            response.put("processingId", processingId);
            return new ResponseEntity<>(response, HttpStatus.OK);
        } catch (Exception e) {
            logger.severe("Error starting file processing: " + e.getMessage());
            processingStatus.put(processingId, "Error starting file processing: " + e.getMessage());
            return new ResponseEntity<>(HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @PostMapping("/upload/json")
    public String receiveData(@RequestBody Map<String, String> data) {
        String merchantName = data.get("merchant_name");
        String pincodes = data.get("pincodes");

        System.out.println("Merchant Name: " + merchantName);
        System.out.println("Pincodes: " + pincodes);

        if (merchantName != null && pincodes != null) {
            String[] pincodeArray = pincodes.split(",");
            for (String pincode : pincodeArray) {
                insertJSONIntoHBase(merchantName, pincode.trim());
            }
        }

        return "Data received successfully!";
    }

    @Async
    public void parseAndSendCSV(MultipartFile file, String processingId) {
        List<Map<String, List<String>>> parsedData = new ArrayList<>();
        try (Reader reader = new BufferedReader(new InputStreamReader(file.getInputStream()))) {
            CSVFormat csvFormat = CSVFormat.DEFAULT.builder()
                    .setHeader()
                    .setSkipHeaderRecord(true)
                    .setIgnoreEmptyLines(true)
                    .build();
            try (CSVParser parser = new CSVParser(reader, csvFormat)) {
                Map<String, List<String>> pinCodeMerchants = new ConcurrentHashMap<>();
                Set<String> uniqueHeaders = new HashSet<>();

                String[] headers = parser.getHeaderMap().keySet().toArray(new String[0]);
                if (headers.length == 0) {
                    throw new IllegalArgumentException("CSV file must have headers.");
                }
                
                loggerx("start of parse");
                
                for (CSVRecord record : parser) {
                    for (int i = 0; i < Math.min(headers.length, record.size()); i++) {
                        String merchantName = record.get(i).trim();
                        if (!merchantName.isEmpty()) {
                            String pinCode = headers[i].trim();
                            pinCodeMerchants.computeIfAbsent(pinCode, k -> new ArrayList<>()).add(merchantName);
                            uniqueHeaders.add(pinCode);
                        }
                    }
                }

                if (!pinCodeMerchants.isEmpty()) {
                    parsedData.add(pinCodeMerchants);
                }

                logger.info("CSV parsed successfully, number of batches: " + parsedData.size());
                loggerx("End of parse");
                processingStatus.put(processingId, "CSV parsed successfully, number of batches: " + parsedData.size());
                parsedDataMap.put(processingId, parsedData);
                parsedData.forEach(batch -> insertBatchIntoHBase(batch, processingId));
            }
        } catch (Exception e) {
            logger.severe("Error parsing CSV file: " + e.getMessage());
            processingStatus.put(processingId, "Error parsing CSV file: " + e.getMessage());
        }
    }

    private String fetchExistingDataFromHBase(String pinCode) throws Exception {
        try (Connection connection = ConnectionFactory.createConnection(hbaseConfig);
             Table table = connection.getTable(TableName.valueOf("pincode_serviceability"))) {
            
            Get get = new Get(Bytes.toBytes(pinCode));
            Result result = table.get(get);
            byte[] value = result.getValue(Bytes.toBytes("cf"), Bytes.toBytes("merchant_id"));
            
            return value != null ? Bytes.toString(value) : null;
        }
    }

    private boolean merchantExists(String existingData, String merchant) {
        if (existingData == null || existingData.isEmpty()) {
            return false;
        }
        String[] merchants = existingData.split(",");
        return Arrays.asList(merchants).contains(merchant);
    }

    @Async
    public void insertBatchIntoHBase(Map<String, List<String>> batch, String processingId) {
        try (Connection connection = ConnectionFactory.createConnection(hbaseConfig);
             Table table = connection.getTable(TableName.valueOf("pincode_serviceability"))) {
            
            for (Map.Entry<String, List<String>> entry : batch.entrySet()) {
                String pinCode = entry.getKey();
                List<String> newMerchants = entry.getValue();

                // Fetch existing data
                String existingData = fetchExistingDataFromHBase(pinCode);
                Set<String> updatedMerchantsSet = new HashSet<>(newMerchants);

                if (existingData != null) {
                    String[] existingMerchants = existingData.split(",");
                    updatedMerchantsSet.addAll(Arrays.asList(existingMerchants));
                }

                String updatedData = String.join(",", updatedMerchantsSet);

                Put put = new Put(Bytes.toBytes(pinCode));
                put.addColumn(Bytes.toBytes("cf"), Bytes.toBytes("merchant_id"), Bytes.toBytes(updatedData));
                table.put(put);
                setcnt++;
            }

            loggerx("Entered " + setcnt + " Rows into HBASE");
            setcnt = 0;
            logger.info("Batch inserted into HBase: " + batch.toString());
            processingStatus.put(processingId, "Batch inserted into HBase successfully.");
        } catch (Exception e) {
            logger.severe("Error inserting batch into HBase: " + e.getMessage());
            processingStatus.put(processingId, "Error inserting batch into HBase: " + e.getMessage());
        }
    }

    @Async
    public void insertJSONIntoHBase(String merchant, String pin) {
        try (Connection connection = ConnectionFactory.createConnection(hbaseConfig);
             Table table = connection.getTable(TableName.valueOf("pincode_serviceability"))) {

            // Fetch existing data
            String existingData = fetchExistingDataFromHBase(pin);

            // Check if the merchant already exists
            if (!merchantExists(existingData, merchant)) {
                String updatedData = existingData == null ? merchant : existingData + "," + merchant;
                Put put = new Put(Bytes.toBytes(pin));
                put.addColumn(Bytes.toBytes("cf"), Bytes.toBytes("merchant_id"), Bytes.toBytes(updatedData));
                table.put(put);
            }

        } catch (Exception e) {
            System.out.println("Error: " + e.getMessage());
        }
    }

    @GetMapping(value = "/upload/status/{processingId}")
    public ResponseEntity<Map<String, Object>> getStatus(@PathVariable String processingId) {
        String status = processingStatus.get(processingId);
        if (status != null) {
            Map<String, Object> response = new HashMap<>();
            response.put("status", status);
            response.put("parsedData", parsedDataMap.get(processingId));
            return new ResponseEntity<>(response, HttpStatus.OK);
        } else {
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }
    }

    public static void loggerx(String txt){
        System.out.println("########################################");
        System.out.println();
        System.out.println();
        System.out.println("            "+txt+"                   ");
        System.out.println();
        System.out.println();
        System.out.println("########################################");
    }
}
