
delete from news_marks;
alter sequence news_marks_id_seq restart with 1;

delete from news_readers;
alter sequence news_readers_id_seq restart with 1;

update twitter_statuses set link_id=NULL, state='none';
delete from news_links;
alter sequence news_links_id_seq restart with 1;
--truncate table news_links restart identity;
