-- Current settings
ALTER SYSTEM SET max_connections = '600';
ALTER SYSTEM SET shared_buffers = '125GB';
ALTER SYSTEM SET effective_cache_size = '72192MB';
ALTER SYSTEM SET checkpoint_completion_target = '0.7';
ALTER SYSTEM SET min_wal_size = '1GB';
ALTER SYSTEM SET max_wal_size = '4GB';
ALTER SYSTEM SET maintenance_work_mem = '25GB';


-- Value that the planner will take in consideration to perform.
ALTER SYSTEM SET effective_cache_size = '375GB'; -- 72GB Before

 -- Higher Value will make restore of checkpoints faster
ALTER SYSTEM SET checkpoint_completion_target = '0.9';  -- 0.7 Before

-- Reserverd Memory for planning 600 connections
ALTER SYSTEM SET max_connections = '600'; -- This defines values above
ALTER SYSTEM SET work_mem = '60MB'; -- 192MB Before

-- Reserverd Memory for planning 200 connections
ALTER SYSTEM SET max_connections = '200'; -- This defines values above
ALTER SYSTEM SET work_mem = '190MB'; -- 192MB Before

-- Better handle transaction spikes
ALTER SYSTEM SET min_wal_size = '4GB'; -- 1GB Before
ALTER SYSTEM SET max_wal_size = '8GB'; -- 4GB Before

-- The amount of memory that workers will allocate when reindexing and vacuum.
-- High values could lead to stale connections, and bad performance on spikes
-- This will be used on schedule or manually
ALTER SYSTEM SET maintenance_work_mem = '5GB'; -- 25GB Before
