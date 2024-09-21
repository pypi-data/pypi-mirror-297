########################################################################################################################
# IMPORTS

import base64
import boto3
import logging
import time

import clickhouse_driver
import requests
from .alchemy import AlchemyInterface
from sqlalchemy import text

########################################################################################################################
# CLASSES

logger = logging.getLogger(__name__)


class PostgresPeer:
    def __init__(self, config):
        self.config = config["db"]
        self.alchemy_interface = AlchemyInterface(config)
        self.engine = self.alchemy_interface.engine

    def create_user(self):
        user = self.config["user"]
        password = self.config["password"]

        logger.info(f"Creating PostgreSQL user '{user}' for database: {self.config['database']}")

        with self.engine.connect() as conn:
            conn.execute(
                text(f"""
            DO $$
            BEGIN
                IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = '{user}') THEN
                    CREATE USER {user} WITH PASSWORD '{password}';
                    ALTER USER {user} REPLICATION;
                    GRANT CREATE ON DATABASE datamarket TO {user};
                END IF;
            END
            $$;
            """)
            )
        logger.info(f"PostgreSQL user '{user}' created or already exists")

    def grant_permissions(self, schema_name):
        user = self.config["user"]

        logger.info(f"Granting permissions for schema '{schema_name}' to '{user}'")

        with self.engine.connect() as conn:
            conn.execute(
                text(f"""
            GRANT USAGE ON SCHEMA "{schema_name}" TO {user};
            GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA "{schema_name}" TO {user};
            ALTER DEFAULT PRIVILEGES IN SCHEMA "{schema_name}" GRANT ALL PRIVILEGES ON TABLES TO {user};
            """)
            )
        logger.info(f"Permissions granted for schema '{schema_name}' to '{user}'")

    def create_publication(self, schema_name, table_names):
        logger.info(f"Creating publication '{schema_name}_peerdb' for schema: {schema_name}")
        with self.engine.connect() as conn:
            conn.execute(text(f"DROP PUBLICATION IF EXISTS {schema_name}_peerdb"))

            table_list = ", ".join([f"{schema_name}.{table}" for table in table_names])
            conn.execute(
                text(f"""
            CREATE PUBLICATION {schema_name}_peerdb FOR TABLE {table_list};
            """)
            )
        logger.info(f"Publication '{schema_name}_peerdb' created successfully")

    def create_tables(self, schema_tables, drop=False):
        logger.info(f"Creating tables in database: {self.config['database']}")
        self.alchemy_interface.reset_db(schema_tables, drop)
        logger.info(f"Tables {'dropped and ' if drop else ''}created successfully")

    def drop_replication_slot(self, schema_name):
        logger.info(f"Checking and dropping replication slot for schema: {schema_name}")
        slot_name = f"peerflow_slot_{schema_name}"

        with self.engine.connect() as conn:
            conn.execute(
                text("""
                SELECT pg_drop_replication_slot(:slot_name)
                WHERE EXISTS (SELECT 1 FROM pg_replication_slots WHERE slot_name = :slot_name)
                """),
                {"slot_name": slot_name},
            )
            logger.info(f"Replication slot '{slot_name}' dropped if it existed")


class ClickhousePeer:
    def __init__(self, config):
        self.config = config["clickhouse"]
        self.ensure_database_exists()
        self.client = clickhouse_driver.Client(
            host=self.config["host"],
            port=self.config["port"],
            user=self.config["user"],
            password=self.config["password"],
            database=self.config["database"],
        )

    def ensure_database_exists(self):
        logger.info(f"Checking if database '{self.config['database']}' exists in Clickhouse")
        temp_client = clickhouse_driver.Client(
            host=self.config["host"],
            port=self.config["port"],
            user=self.config["user"],
            password=self.config["password"],
        )

        databases = temp_client.execute("SHOW DATABASES")
        if (self.config["database"],) not in databases:
            logger.info(f"Database '{self.config['database']}' does not exist. Creating it now.")
            temp_client.execute(f"CREATE DATABASE IF NOT EXISTS {self.config['database']}")
            logger.info(f"Database '{self.config['database']}' created successfully")
        else:
            logger.info(f"Database '{self.config['database']}' already exists")

    def delete_existing_tables(self, table_names):
        logger.info(f"Deleting existing tables in Clickhouse for database: {self.config['database']}")

        all_tables = self.client.execute("SHOW TABLES")
        all_tables = [table[0] for table in all_tables]

        # Delete tables containing "peerdb" in their names
        for table in all_tables:
            if "peerdb" in table.lower():
                self.client.execute(f"DROP TABLE IF EXISTS {table}")
                logger.info(f"Deleted table: {table}")

        # Delete tables passed through run_automation and their "_resync" variants
        for table in table_names:
            if table in all_tables:
                self.client.execute(f"DROP TABLE IF EXISTS {table}")
                logger.info(f"Deleted table: {table}")

            resync_table = f"{table}_resync"
            if resync_table in all_tables:
                self.client.execute(f"DROP TABLE IF EXISTS {resync_table}")
                logger.info(f"Deleted table: {resync_table}")

        logger.info("Finished deleting existing tables in Clickhouse")

    def create_row_policies(self, schema_name, table_names):
        logger.info(f"Creating row policies for schema: {schema_name}")
        for table_name in table_names:
            policy_name = "non_deleted"
            query = f"""
            CREATE ROW POLICY IF NOT EXISTS {policy_name} ON {schema_name}.{table_name}
            FOR SELECT USING _peerdb_is_deleted = 0
            """
            self.client.execute(query)
            logger.info(f"Created row policy '{policy_name}' for table '{table_name}'")


class TransientS3:
    def __init__(self, config):
        self.config = config["peerdb-s3"]
        self.s3_client = boto3.Session(profile_name=self.config["profile"]).client("s3")
        self.bucket_name = self.config["bucket"]

    def delete_paths_with_schema(self, schema_name):
        logger.info(f"Deleting paths containing '{schema_name}' from S3")

        paginator = self.s3_client.get_paginator("list_objects_v2")
        pages = paginator.paginate(Bucket=self.bucket_name, Delimiter="/")

        for page in pages:
            if "CommonPrefixes" in page:
                for prefix in page["CommonPrefixes"]:
                    folder = prefix["Prefix"]
                    if schema_name in folder:
                        self._delete_folder_contents(folder)

        logger.info(f"Deleted paths containing '{schema_name}' from S3")

    def _delete_folder_contents(self, folder):
        logger.info(f"Deleting contents of folder: {folder}")

        paginator = self.s3_client.get_paginator("list_objects_v2")
        pages = paginator.paginate(Bucket=self.bucket_name, Prefix=folder)

        delete_us = dict(Objects=[])
        for page in pages:
            if "Contents" in page:
                for obj in page["Contents"]:
                    delete_us["Objects"].append(dict(Key=obj["Key"]))

                    # AWS limits to deleting 1000 objects at a time
                    if len(delete_us["Objects"]) >= 1000:
                        self.s3_client.delete_objects(Bucket=self.bucket_name, Delete=delete_us)
                        delete_us = dict(Objects=[])

        if len(delete_us["Objects"]):
            self.s3_client.delete_objects(Bucket=self.bucket_name, Delete=delete_us)

        logger.info(f"Deleted contents of folder: {folder}")


class PeerDBInterface:
    def __init__(self, config):
        self.config = config["peerdb"]
        self.source = PostgresPeer(config)
        self.destination = ClickhousePeer(config)
        self.transient_s3 = TransientS3(config)

    def _make_api_request(self, endpoint, payload):
        url = f"http://{self.config['host']}:{self.config['port']}/api/{endpoint}"
        password = self.config["password"]
        credentials = f":{password}"
        encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")

        headers = {"Authorization": f"Basic {encoded_credentials}", "Content-Type": "application/json"}

        logger.info(f"Making API request to PeerDB endpoint: {endpoint}")
        try:
            r = requests.post(url, headers=headers, json=payload, timeout=30)
            r.raise_for_status()
            logger.info(f"API request to {endpoint} completed successfully")
            return r.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error occurred: {e}")
            logger.error(f"Response JSON: {r.json()}")
            raise

    def create_postgres_peer(self):
        logger.info(f"Creating Postgres peer for database: {self.source.config['database']}")
        payload = {
            "peer": {
                "name": self.source.config["database"],
                "type": 3,
                "postgres_config": {
                    "host": self.source.config["host"],
                    "port": int(self.source.config["admin_port"]),
                    "user": self.config["user"],
                    "password": self.config["password"],
                    "database": self.source.config["database"],
                },
            },
            "allow_update": True,
        }

        response = self._make_api_request("v1/peers/create", payload)
        if response.get("status") == "FAILED":
            raise Exception(f"Failed to create Postgres peer: {response.get('message', 'Unknown error')}")

        logger.info(f"Postgres peer for database '{self.source.config['database']}' created successfully")

    def create_clickhouse_peer(self, schema_name):
        logger.info(f"Creating Clickhouse peer for schema: {schema_name}")

        payload = {
            "peer": {
                "name": f"{schema_name}",
                "type": 8,
                "clickhouse_config": {
                    "host": self.destination.config["host"],
                    "port": int(self.destination.config["port"]),
                    "user": self.destination.config["user"],
                    "password": self.destination.config["password"],
                    "database": schema_name,
                    "disable_tls": True,
                    "s3_path": f"s3://{self.transient_s3.config['bucket']}",
                    "access_key_id": self.transient_s3.config["access_key_id"],
                    "secret_access_key": self.transient_s3.config["secret_access_key"],
                    "region": "local",
                    "endpoint": f"http://{self.transient_s3.config['host']}:{self.transient_s3.config['port']}",
                },
            },
            "allow_update": True,
        }

        response = self._make_api_request("v1/peers/create", payload)
        if response.get("status") == "FAILED":
            raise Exception(f"Failed to create Clickhouse peer: {response.get('message', 'Unknown error')}")

        logger.info(f"Clickhouse peer for schema '{schema_name}' created successfully")

    def drop_mirror(self, schema_name):
        logger.info(f"Dropping mirror for schema: {schema_name}")

        payload = {"flowJobName": f"{schema_name}", "requestedFlowState": "STATUS_TERMINATED"}

        mirror_status = self.check_mirror_status(schema_name)
        if mirror_status == "STATUS_UNKNOWN":
            logger.info(f"Mirror for schema '{schema_name}' does not exist, no need to drop.")
            return

        response = self._make_api_request("v1/mirrors/state_change", payload)
        if not bool(response.get("ok", "true")) or int(response.get("code", 0)) == 2:
            raise Exception(
                f"Failed to drop mirror for schema '{schema_name}': {response.get('errorMessage', response.get('message', 'Unknown error'))}"
            )

        logger.info(f"Mirror for schema '{schema_name}' dropped successfully")

    def check_mirror_status(self, schema_name):
        logger.info(f"Checking mirror status for schema: {schema_name}")
        max_attempts = 60
        attempt = 0
        while attempt < max_attempts:
            payload = {"flowJobName": schema_name, "includeFlowInfo": False}
            response = self._make_api_request("v1/mirrors/status", payload)
            current_state = response.get("currentFlowState")

            if current_state != "STATUS_SETUP":
                logger.info(f"Mirror status for schema '{schema_name}' is: {current_state}")
                return current_state

            attempt += 1
            time.sleep(10)

        logger.warning(f"Mirror status check timed out for schema: {schema_name}")
        return None

    def resync_operations(self, schema_name, table_names, resync, hard_resync):
        if resync:
            logger.info(f"Resync requested. Performing {'hard' if hard_resync else 'simple'} resync operations.")
            self.drop_mirror(schema_name)
            self.transient_s3.delete_paths_with_schema(schema_name)
            if hard_resync:
                self.destination.delete_existing_tables(table_names)
                self.source.drop_replication_slot(schema_name)
            logger.info("Resync operations completed.")

    def create_mirror(self, schema_name, table_names, resync, hard_resync):
        self.resync_operations(schema_name, table_names, resync, hard_resync)
        logger.info(f"Creating mirror for schema: {schema_name}")

        table_mappings = [
            {"source_table_identifier": f"{schema_name}.{table}", "destination_table_identifier": f"{table}"}
            for table in table_names
        ]

        payload = {
            "connection_configs": {
                "flow_job_name": f"{schema_name}",
                "source_name": self.source.config["database"],
                "destination_name": f"{schema_name}",
                "table_mappings": table_mappings,
                "max_batch_size": 1000000,
                "idle_timeout_seconds": 10,
                "publication_name": f"{schema_name}_peerdb",
                "do_initial_snapshot": True,
                "snapshot_num_rows_per_partition": 1000000,
                "snapshot_max_parallel_workers": 1,
                "snapshot_num_tables_in_parallel": 1,
                "resync": not hard_resync,
                "initial_snapshot_only": False,
                "soft_delete_col_name": "_peerdb_is_deleted",
                "synced_at_col_name": "_peerdb_synced_at",
            }
        }

        response = self._make_api_request("v1/flows/cdc/create", payload)
        if not bool(response.get("ok", "true")) or int(response.get("code", 0)) == 2:
            raise Exception(
                f"Failed to create mirror for schema '{schema_name}': {response.get('errorMessage', response.get('message', 'Unknown error'))}"
            )

        mirror_status = self.check_mirror_status(schema_name)
        if mirror_status:
            logger.info(f"Mirror status for schema '{schema_name}' is: {mirror_status}")
            logger.info(f"Mirror creation for schema '{schema_name}' completed successfully")
        else:
            logger.warning(f"Failed to confirm mirror status change for schema: {schema_name}")

    def run_automation(self, schema_name, schema_tables, drop=False, resync=False, hard_resync=False):
        logger.info(f"Starting automation for schema: {schema_name}")

        table_names = [table.__tablename__ for table in schema_tables]

        self.source.create_user()
        self.source.create_tables(schema_tables, drop)
        self.source.grant_permissions(schema_name)
        self.source.create_publication(schema_name, table_names)
        self.create_postgres_peer()
        self.create_clickhouse_peer(schema_name)
        self.create_mirror(schema_name, table_names, resync, hard_resync)
        self.destination.create_row_policies(schema_name, table_names)

        logger.info(f"Automation completed successfully for schema: {schema_name}")
