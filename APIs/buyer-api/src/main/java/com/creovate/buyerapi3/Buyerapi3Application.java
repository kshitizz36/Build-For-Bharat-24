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



import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@SpringBootApplication
public class Buyerapi3Application {


	public static String hbaseConn(int pin){
		Configuration config = HBaseConfiguration.create();
        config.set("hbase.zookeeper.quorum", "34.93.220.20"); // Replace with your HBase Zookeeper quorum
        config.set("hbase.zookeeper.property.clientPort", "2181"); // Replace with your Zookeeper client port if different

        try (Connection connection = ConnectionFactory.createConnection(config);
             Table table = connection.getTable(TableName.valueOf("pincode_serviceability"))) {

            String pincode = "123456"; // Example pincode to query
            Get get = new Get(Bytes.toBytes(pincode));
            Result result = table.get(get);
            byte[] value = result.getValue(Bytes.toBytes("cf"), Bytes.toBytes("merchants"));

            if (value != null) {
                String merchants = Bytes.toString(value);
                System.out.println("Pincode: " + pincode + ", Merchants: " + merchants);
            } else {
                System.out.println("No merchants found for pincode: " + pincode);
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
		return "yo";
	}

	public static void main(String[] args) {
		SpringApplication.run(Buyerapi3Application.class, args);
	}

	@RestController
    public class HBaseController {


        @GetMapping("/getMerchants")
        public String getMerchants(@RequestParam String pincode) {
            System.out.println(pincode);
			hbaseConn(Integer.parseInt(pincode));
			return "hello";
        }
    }

}
