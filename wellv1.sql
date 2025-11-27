create table well (
    uwi varchar primary key
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