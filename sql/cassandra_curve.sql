CREATE KEYSPACE IF NOT EXISTS well_logs
WITH REPLICATION = {
  'class':'SimpleStrategy',
  'replication_factor': 1
};

USE well_logs;

CREATE TABLE IF NOT EXISTS curve_info (
    uwi TEXT PRIMARY KEY,
    mnemonics LIST<INT>,
    chunks INT,
    chunk_size INT
);

CREATE TABLE curve_chunk (
    uwi TEXT,
    chunk_index INT,
    chunk_min TEXT,
    chunk_max TEXT,
    mnemonic_id INT,
    values LIST<TEXT>,
    PRIMARY KEY ((uwi, chunk_index), mnemonic_id)
) WITH CLUSTERING ORDER BY (mnemonic_id ASC);

