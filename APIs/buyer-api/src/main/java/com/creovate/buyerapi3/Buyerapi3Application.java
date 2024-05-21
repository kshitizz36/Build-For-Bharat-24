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
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@SpringBootApplication
public class Buyerapi3Application {

    static final String hbaseIP = "34.93.220.20";


	public static String hbaseConn(String pin){
		Configuration config = HBaseConfiguration.create();
        config.set("hbase.zookeeper.quorum", hbaseIP); 
        config.set("hbase.zookeeper.property.clientPort", "2181"); 

        try (Connection connection = ConnectionFactory.createConnection(config);
             Table table = connection.getTable(TableName.valueOf("pincode_serviceability"))) {

            Get get = new Get(Bytes.toBytes(pin));
            Result result = table.get(get);
            byte[] value = result.getValue(Bytes.toBytes("cf"), Bytes.toBytes("merchants"));

            if (value != null) {
                String merchants = Bytes.toString(value);
                logger(" "+pin+"  -> "+merchants);
                return merchants;
            } else {
                logger("NO MERCHANTS FOUND FOR "+pin);
                return "No Merchants Found";
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
		return "Null";
	}

	public static void main(String[] args) {
		SpringApplication.run(Buyerapi3Application.class, args);
	}


    public static void logger(String txt){
        System.out.println("########################################");
        System.out.println();
        System.out.println();
        System.out.println("            "+txt+"                   ");
        System.out.println();
        System.out.println();
        System.out.println("########################################");

    }

	@RestController
    public class HBaseController {


        @GetMapping("/getMerchants")
        public String getMerchants(@RequestParam String pincode) {
            logger("GET REQUEST FOR "+pincode);
			String merch = hbaseConn(pincode);
			return merch;
        }
    }

}
