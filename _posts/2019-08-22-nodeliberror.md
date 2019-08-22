---
layout: post
date: 2019-08-22 02:00:00
categories: EventStreams
title: "Error while installing node-rdkafka on MacOs - Undefined symbols for architecture x86_64"
---

During npm install you my recieve an `Undefined symbols for architecture x86_64:` like below. In order to get around this you must install librdkafka.

<!--more-->


```bash
gcc -L/Users/chris/src/event-streams-samples/kafka-nodejs-console-sample/node_modules/node-rdkafka/build/deps -shared -dynamiclib -Wl,-install_name,/Users/chris/src/event-streams-samples/kafka-nodejs-console-sample/node_modules/node-rdkafka/build/deps/librdkafka.1.dylib rdkafka.o rdkafka_broker.o rdkafka_msg.o rdkafka_topic.o rdkafka_conf.o rdkafka_timer.o rdkafka_offset.o rdkafka_transport.o rdkafka_buf.o rdkafka_queue.o rdkafka_op.o rdkafka_request.o rdkafka_cgrp.o rdkafka_pattern.o rdkafka_partition.o rdkafka_subscription.o rdkafka_assignor.o rdkafka_range_assignor.o rdkafka_roundrobin_assignor.o rdkafka_feature.o rdcrc32.o crc32c.o rdmurmur2.o rdaddr.o rdrand.o rdlist.o tinycthread.o rdlog.o rdstring.o rdkafka_event.o rdkafka_metadata.o rdregex.o rdports.o rdkafka_metadata_cache.o rdavl.o rdkafka_sasl.o rdkafka_sasl_plain.o rdkafka_interceptor.o rdkafka_msgset_writer.o rdkafka_msgset_reader.o rdkafka_header.o rdkafka_admin.o rdkafka_aux.o rdkafka_background.o rdvarint.o rdbuf.o rdunittest.o rdkafka_sasl_cyrus.o rdkafka_sasl_scram.o snappy.o rdgz.o rdhdrhistogram.o rdkafka_lz4.o xxhash.o lz4.o lz4frame.o lz4hc.o rddl.o rdkafka_plugin.o -o librdkafka.1.dylib -lsasl2 -L/usr/local/Cellar/openssl/1.0.2s/lib -lssl -lm -lz -ldl -lpthread
Undefined symbols for architecture x86_64:
  "_CRYPTO_cleanup_all_ex_data", referenced from:
      _rd_kafka_transport_ssl_term in rdkafka_transport.o
  "_CRYPTO_num_locks", referenced from:
      _rd_kafka_transport_ssl_init in rdkafka_transport.o
  "_CRYPTO_set_id_callback", referenced from:
      _rd_kafka_transport_ssl_term in rdkafka_transport.o
      _rd_kafka_transport_ssl_init in rdkafka_transport.o
  "_CRYPTO_set_locking_callback", referenced from:
      _rd_kafka_transport_ssl_term in rdkafka_transport.o
      _rd_kafka_transport_ssl_init in rdkafka_transport.o
  "_ERR_clear_error", referenced from:
      _rd_kafka_transport_send in rdkafka_transport.o
      _rd_kafka_transport_recv in rdkafka_transport.o
      _rd_kafka_transport_io_serve in rdkafka_transport.o
  "_ERR_error_string_n", referenced from:
      _rd_kafka_ssl_error in rdkafka_transport.o
  "_ERR_get_error_line_data", referenced from:
      _rd_kafka_ssl_error in rdkafka_transport.o
  "_ERR_peek_error", referenced from:
      _rd_kafka_transport_ssl_io_update in rdkafka_transport.o
  "_ERR_remove_thread_state", referenced from:
      _rd_kafka_broker_thread_main in rdkafka_broker.o
  "_EVP_DecodeBlock", referenced from:
      _rd_kafka_sasl_scram_fsm in rdkafka_sasl_scram.o
  "_EVP_EncodeBlock", referenced from:
      _rd_kafka_sasl_scram_build_client_final_message in rdkafka_sasl_scram.o
  "_EVP_PKEY_free", referenced from:
      _rd_kafka_transport_ssl_ctx_init in rdkafka_transport.o
  "_EVP_PKEY_new", referenced from:
      _rd_kafka_transport_ssl_ctx_init in rdkafka_transport.o
  "_EVP_sha1", referenced from:
      _rd_kafka_sasl_scram_conf_validate in rdkafka_sasl_scram.o
  "_EVP_sha256", referenced from:
      _rd_kafka_sasl_scram_conf_validate in rdkafka_sasl_scram.o
  "_EVP_sha512", referenced from:
      _rd_kafka_sasl_scram_conf_validate in rdkafka_sasl_scram.o
  "_HMAC", referenced from:
      _rd_kafka_sasl_scram_Hi in rdkafka_sasl_scram.o
      _rd_kafka_sasl_scram_HMAC in rdkafka_sasl_scram.o
  "_OPENSSL_add_all_algorithms_noconf", referenced from:
      _rd_kafka_transport_ssl_init in rdkafka_transport.o
  "_PKCS12_free", referenced from:
      _rd_kafka_transport_ssl_ctx_init in rdkafka_transport.o
  "_PKCS12_parse", referenced from:
      _rd_kafka_transport_ssl_ctx_init in rdkafka_transport.o
  "_SHA1", referenced from:
      _rd_kafka_sasl_scram_conf_validate in rdkafka_sasl_scram.o
  "_SHA256", referenced from:
      _rd_kafka_sasl_scram_conf_validate in rdkafka_sasl_scram.o
  "_SHA512", referenced from:
      _rd_kafka_sasl_scram_conf_validate in rdkafka_sasl_scram.o
  "_X509_STORE_set_flags", referenced from:
      _rd_kafka_transport_ssl_ctx_init in rdkafka_transport.o
  "_X509_free", referenced from:
      _rd_kafka_transport_ssl_ctx_init in rdkafka_transport.o
      _rd_kafka_transport_io_serve in rdkafka_transport.o
  "_X509_new", referenced from:
      _rd_kafka_transport_ssl_ctx_init in rdkafka_transport.o
  "_X509_verify_cert_error_string", referenced from:
      _rd_kafka_transport_io_serve in rdkafka_transport.o
  "_d2i_PKCS12_fp", referenced from:
      _rd_kafka_transport_ssl_ctx_init in rdkafka_transport.o
  "_sk_pop_free", referenced from:
      _rd_kafka_transport_ssl_ctx_init in rdkafka_transport.o
ld: symbol(s) not found for architecture x86_64
clang: error: linker command failed with exit code 1 (use -v to see invocation)
make[2]: *** [librdkafka.1.dylib] Error 1
make[1]: *** [libs] Error 2
make: *** [11a9e3388a67e1ca5c31c1d8da49cb6d2714eb41.intermediate] Error 2
rm 11a9e3388a67e1ca5c31c1d8da49cb6d2714eb41.intermediate
```


In order to fix this issue install librdkafka
```
brew install librdkafka
export BUILD_LIBRDKAFKA=0
npm install
```

*If you are running node 12.x npm will fail. Current advise is to roll back to node 10. *

Information came from https://github.com/Blizzard/node-rdkafka/issues/481
