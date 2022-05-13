create table cqpocsredshiftdemo (
  industry_name_ANZSIC varchar(100)    not null,
  rme_size_grp     	   varchar(100)    not null,
  variables        	   varchar(100)    not null
)

Select * from cqpocsredshiftdemo

INSERT INTO cqpocsredshiftdemo (industry_name_ANZSIC,rme_size_grp,variables) VALUES ('RRR', 'Paul', 'xyz');
