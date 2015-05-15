set @firstday = '2015-03-02';

-- Compute the number of books were added between firstday and one week after firstday
set @book_add_per_week = (
select count(*)
	from (
		select b.uuid as uuid, b.title as title, b.authors as author, count(lc.id) as count
        from library_cards as lc
        join documents as d on lc.document_id = d.id
        join books as b on b.id = d.book_id
        left join list_documents as ld on ld.book_id = b.id
        where lc.created_at between @firstday and @firstday + interval 1 week
        and lc.state != 'removed'
        and d.language = 'ru'
        -- Excluding private and free books 0b110101 == 53
        AND NOT (b.flags & 53)
        -- Excluding auto-added editorial intro books
        AND b.id
        NOT IN (
           382385,
           348212,
           349139,
           285852,
           286592,
           11833,
           300047,
           30026
        )
        AND ld.book_id is null
        group by b.uuid, b.title, b.authors
        )book_add_per_week);

-- Compute the number of books were added between one year before firstday and firstday        
set @book_add_per_year = (
select count(*)
	from (
		select b.uuid as uuid, b.title as title, b.authors as author, count(lc.id) as count
        from library_cards as lc
        join documents as d on lc.document_id = d.id
        join books as b on b.id = d.book_id
        left join list_documents as ld on ld.book_id = b.id
        where lc.created_at between @firstday - interval 1 year and @firstday
        and lc.state != 'removed'
        and d.language = 'ru'
        -- Excluding private and free books 0b110101 == 53
        AND NOT (b.flags & 53)
        -- Excluding auto-added editorial intro books
        AND b.id
        NOT IN (
           382385,
           348212,
           349139,
           285852,
           286592,
           11833,
           300047,
           30026
        )
        AND ld.book_id is null
        group by b.uuid, b.title, b.authors
        )book_add_per_year);
      
select @rank := @rank + 1 as rank, book, TF_IDF, cntcnt from 

(select (TF*IDF) as TF_IDF, this_week.book, this_week.cntcnt

from 
(
-- Compute TF for each book as a number of book additions per week divided by @book_add_per_week  
select uuid, title, concat(author, ', "', title, '"') as book, count/@book_add_per_week as TF, count as cntcnt
    from (
        select b.uuid as uuid, b.title as title, b.authors as author, count(lc.id) as count
        from library_cards as lc
        join documents as d on lc.document_id = d.id
        join books as b on b.id = d.book_id
        left join list_documents as ld on ld.book_id = b.id
        where lc.created_at between @firstday and @firstday + interval 1 week
        and lc.state != 'removed'
        and d.language = 'ru'
        -- Excluding private and free books 0b110101 == 53
        AND NOT (b.flags & 53)
        -- Excluding auto-added editorial intro books
        AND b.id
        NOT IN (
           382385,
           348212,
           349139,
           285852,
           286592,
           11833,
           300047,
           30026
        )
        AND ld.book_id is null
        group by b.uuid, b.title, b.authors
    ) as b) this_week

    inner join

-- Compute IDF for each book as a @book_add_per_year divided by the number of book additions per year
(select 
        uuid, title, LOG(@book_add_per_year/count) as IDF
    from (
        select b.uuid as uuid, b.title as title, b.authors as author, count(lc.id) as count
        from library_cards as lc
        join documents as d on lc.document_id = d.id
        join books as b on b.id = d.book_id
        left join list_documents as ld on ld.book_id = b.id
        where lc.created_at between @firstday - interval 1 year and @firstday
        and lc.state != 'removed'
        and d.language = 'ru'
        -- Excluding private and free books 0b110101 == 53
        AND NOT (b.flags & 53)
        -- Excluding auto-added editorial intro books
        AND b.id
        NOT IN (
           382385,
           348212,
           349139,
           285852,
           286592,
           11833,
           300047,
           30026
        )
        AND ld.book_id is null
        group by b.uuid, b.title, b.authors
    ) as b) this_year
    
on this_week.uuid = this_year.uuid
order by TF_IDF desc
limit 100
) as main,
(SELECT @rank := 0) as r
limit 20; 
    
    
