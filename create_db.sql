-- create_db.sql (Smart Grid Energy Consumption Database)

-- Drop tables in reverse FK dependency order

BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE energy_readings CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/
BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE meter_locations CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/
BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE smart_meters CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/
BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE household_to_rate_plans CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/
BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE rate_plans CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/
BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE households CASCADE CONSTRAINTS';
EXCEPTION WHEN OTHERS THEN NULL;
END;
/

-- Drop sequences if they exist
BEGIN EXECUTE IMMEDIATE 'DROP SEQUENCE households_seq';   EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP SEQUENCE rate_plans_seq';   EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP SEQUENCE smart_meters_seq'; EXCEPTION WHEN OTHERS THEN NULL; END;
/


--1 households
CREATE TABLE households (
    id                INTEGER       NOT NULL,
    address           VARCHAR2(255) NOT NULL,
    city              VARCHAR2(100) NOT NULL,
    state             VARCHAR2(50),
    zip_code          VARCHAR2(20),
    installation_date DATE,
    CONSTRAINT pk_households PRIMARY KEY (id)
);

CREATE SEQUENCE households_seq START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;

CREATE OR REPLACE TRIGGER trg_households_bi
BEFORE INSERT ON households
FOR EACH ROW
WHEN (NEW.id IS NULL)
BEGIN
    :NEW.id := households_seq.NEXTVAL;
END;
/


--2 rate_plans
CREATE TABLE rate_plans (
    id                   INTEGER       NOT NULL,
    plan_name            VARCHAR2(100) NOT NULL,
    base_rate_per_kwh    NUMBER(10,4)  NOT NULL,
    peak_rate_per_kwh    NUMBER(10,4),
    effective_start_date DATE,
    effective_end_date   DATE,
    CONSTRAINT pk_rate_plans PRIMARY KEY (id)
);

CREATE SEQUENCE rate_plans_seq START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;

CREATE OR REPLACE TRIGGER trg_rate_plans_bi
BEFORE INSERT ON rate_plans
FOR EACH ROW
WHEN (NEW.id IS NULL)
BEGIN
    :NEW.id := rate_plans_seq.NEXTVAL;
END;
/

--3 household_to_rate_plans  (junction / bridge table)
CREATE TABLE household_to_rate_plans (
    household_id  INTEGER NOT NULL,
    rate_plan_id  INTEGER NOT NULL,
    start_date    DATE    NOT NULL,
    end_date      DATE,
    CONSTRAINT pk_h2rp          PRIMARY KEY (household_id, rate_plan_id, start_date),
    CONSTRAINT fk_h2rp_household FOREIGN KEY (household_id) REFERENCES households(id),
    CONSTRAINT fk_h2rp_rate_plan FOREIGN KEY (rate_plan_id) REFERENCES rate_plans(id)
);

--4 smart_meters
CREATE TABLE smart_meters (
    id               INTEGER       NOT NULL,
    serial_number    VARCHAR2(100) NOT NULL,
    manufacturer     VARCHAR2(100),
    firmware_version VARCHAR2(50),
    install_date     DATE          NOT NULL,
    household_id     INTEGER       NOT NULL,
    CONSTRAINT pk_smart_meters PRIMARY KEY (id),
    CONSTRAINT fk_sm_household  FOREIGN KEY (household_id) REFERENCES households(id)
);

CREATE SEQUENCE smart_meters_seq START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;

CREATE OR REPLACE TRIGGER trg_smart_meters_bi
BEFORE INSERT ON smart_meters
FOR EACH ROW
WHEN (NEW.id IS NULL)
BEGIN
    :NEW.id := smart_meters_seq.NEXTVAL;
END;
/

--5 meter_locations
CREATE TABLE meter_locations (
    meter_id           INTEGER     NOT NULL,
    latitude           NUMBER(9,6) NOT NULL,
    longitude          NUMBER(9,6) NOT NULL,
    last_verified_date DATE,
    CONSTRAINT pk_meter_locations PRIMARY KEY (meter_id),
    CONSTRAINT fk_ml_meter        FOREIGN KEY (meter_id) REFERENCES smart_meters(id)
);

--6 energy_readings
CREATE TABLE energy_readings (
    meter_id              INTEGER      NOT NULL,
    reading_timestamp     TIMESTAMP    NOT NULL,
    global_active_power   NUMBER(10,3) NOT NULL,
    global_reactive_power NUMBER(10,3),
    voltage               NUMBER(7,1)  NOT NULL,
    global_intensity      NUMBER(10,2) NOT NULL,
    sub_metering_1        NUMBER(10,2),
    sub_metering_2        NUMBER(10,2),
    sub_metering_3        NUMBER(10,2),
    CONSTRAINT pk_energy_readings PRIMARY KEY (meter_id, reading_timestamp),
    CONSTRAINT fk_er_meter        FOREIGN KEY (meter_id) REFERENCES smart_meters(id)
);
