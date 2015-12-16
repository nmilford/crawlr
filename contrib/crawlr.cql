CREATE KEYSPACE crawlr WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};
USE crawlr;

CREATE TABLE pages ( 
  id bigint,
  url text,
  crawled_at timestamp,
  failure boolean,
  last_failure text,
  title text,
  body text,
  internal_links text,
  outbound_links text,
  PRIMARY KEY (id)
);

CREATE TABLE failure_counts (
  id bigint,
  failures counter,
  PRIMARY KEY (id)
);
