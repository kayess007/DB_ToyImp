create table well (
    uwi varchar primary key
);

create table well_metadata (
    uwi varchar primary key,
    well_name varchar,
    re_entry integer,
    operator varchar,
    surface_lat_n83 varchar,
    surface_lon_n83 varchar,
    land_tenure_area varchar,
    classification varchar,
    datum double precision,
    datum_elevation varchar,
    spud_date varchar,
    release_date varchar,
    foreign key (uwi) references well (uwi)
);

create table mnemonic (
    mnemonic_id integer primary key,
    unit varchar,
    description text
);

create table mnemonic_name (
    mnemonic integer,
    name varchar,
    primary key (mnemonic, name),
    foreign key (mnemonic) references mnemonic (mnemonic_id)
);

create table well_param (
    uwi varchar,
    mnemonic integer,
    value varchar,
    primary key (uwi, mnemonic),
    foreign key (uwi) references well (uwi),
    foreign key (mnemonic) references mnemonic (mnemonic_id)
);

create table curve_param (
    uwi varchar,
    mnemonic integer,
    primary key (uwi, mnemonic),
    foreign key (uwi) references well (uwi),
    foreign key (mnemonic) references mnemonic (mnemonic_id)
);

create table well_curve (
    uwi varchar,
    mnemonic integer,
    row_id integer,
    value varchar,
    primary key (uwi, mnemonic, row_id),
    foreign key (uwi, mnemonic) references curve_param (uwi, mnemonic)
);