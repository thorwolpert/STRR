CREATE TABLE dss_organization (
	organization_id      bigint  NOT NULL GENERATED ALWAYS AS IDENTITY  ,
	organization_type    varchar(25)  NOT NULL  ,
	organization_cd      varchar(25)  NOT NULL  ,
	organization_nm      varchar(250)  NOT NULL  ,
	is_lg_participating  boolean    ,
	is_principal_residence_required boolean    ,
	is_business_licence_required boolean    ,
	area_geometry        geometry    ,
	managing_organization_id bigint    ,
	upd_dtm              timestamptz  NOT NULL  ,
	upd_user_guid        uuid    ,
	CONSTRAINT dss_organization_pk PRIMARY KEY ( organization_id )
 );

ALTER TABLE dss_organization ADD CONSTRAINT dss_organization_fk_managed_by FOREIGN KEY ( managing_organization_id ) REFERENCES dss_organization( organization_id );

CREATE OR REPLACE FUNCTION dss_update_audit_columns()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
BEGIN
    NEW.upd_dtm := current_timestamp;
    RETURN NEW;
END;
$function$;

CREATE TRIGGER dss_organization_br_iu_tr BEFORE INSERT OR UPDATE ON dss_organization FOR EACH ROW EXECUTE FUNCTION dss_update_audit_columns();

COMMENT ON TABLE dss_organization IS 'A private company or governing body component that plays a role in short term rental reporting or enforcement';

COMMENT ON COLUMN dss_organization.organization_id IS 'Unique generated key';

COMMENT ON COLUMN dss_organization.organization_type IS 'Foreign key';

COMMENT ON COLUMN dss_organization.organization_cd IS 'An immutable system code that identifies the organization (e.g. CEU, AIRBNB)';

COMMENT ON COLUMN dss_organization.organization_nm IS 'A human-readable name that identifies the organization (e.g. Corporate Enforecement Unit, City of Victoria)';

COMMENT ON COLUMN dss_organization.is_lg_participating IS 'Indicates whether a LOCAL GOVERNMENT ORGANIZATION participates in Short Term Rental Data Sharing';

COMMENT ON COLUMN dss_organization.is_principal_residence_required IS 'Indicates whether a LOCAL GOVERNMENT SUBDIVISION is subject to Provincial Principal Residence Short Term Rental restrictions';

COMMENT ON COLUMN dss_organization.is_business_licence_required IS 'Indicates whether a LOCAL GOVERNMENT SUBDIVISION requires a business licence for Short Term Rental operation';

COMMENT ON COLUMN dss_organization.area_geometry IS 'the multipolygon shape identifying the boundaries of a local government subdivision';

COMMENT ON COLUMN dss_organization.managing_organization_id IS 'Self-referential hierarchical foreign key';

COMMENT ON COLUMN dss_organization.upd_dtm IS 'Trigger-updated timestamp of last change';

COMMENT ON COLUMN dss_organization.upd_user_guid IS 'The globally unique identifier (assigned by the identity provider) for the most recent user to record a change';