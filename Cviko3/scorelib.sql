
create table person ( id integer primary key not null,
                      born integer,
                      died integer,
                      name varchar not null );

create table score ( id integer primary key not null,
                     genre varchar,
                     key varchar,
                     incipit varchar,
                     year integer );

create table voice ( id integer primary key not null,
                     number integer not null,
                     score integer references score( id ) not null,
                     name varchar );

create table edition ( id integer primary key not null,
                       score integer references score( id ) not null,
                       name varchar,
                       year integer );

create table score_author( id integer primary key not null,
                           score integer references score( id ) not null,
                           composer integer references person( id ) not null );

create table edition_author( id integer primary key not null,
                             edition integer references edition( id ) not null,
                             editor integer references person( id ) not null );

create table print ( id integer primary key not null,
                     partiture varchar(1) default 'N' not null,
                     edition integer references edition( id ) );

