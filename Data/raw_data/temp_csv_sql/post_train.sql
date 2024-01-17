select distinct 
	public.rivers_post.date,	
	snow.snow_height,
	snow.degree_coverage ,
	temperature_precipitation.tmean ,
	post_1,
	post_2,
	/*post_3,*/
	post_4,
	post_5,
	post_6,
	post_7,
	post_8,
	post_9,
	post_10,
	post_11,
	post_9387
from
	public.rivers_post
inner join snow on
	rivers_post.date = snow.date
	and snow.vmo_index = 24908
inner join temperature_precipitation on
	rivers_post.date = temperature_precipitation.date
	and temperature_precipitation.vmo_index = 24908
inner join /*public.rivers_post AS post_9387*/
	(
	select
		public.rivers_post.level_w as post_9387,
		public.rivers_post.date as date_9387
	from
		public.rivers_post
	where
		public.rivers_post.code_post = 9387 )n2
                                    on
	( public.rivers_post.date = n2.date_9387 )
	/*-------------------POST  1---------------------------*/
inner join 
	(
	select
		public.rivers_post.level_w as post_1,
		public.rivers_post.date as date_post_1
	from
		public.rivers_post
	where
		public.rivers_post.code_post = 9393 
	)p1 on ( public.rivers_post.date = p1.date_post_1 )
		/*-------------------POST  2---------------------------*/
inner join 
	(
	select
		public.rivers_post.level_w as post_2,
		public.rivers_post.date as date_post_2
	from
		public.rivers_post
	where
		public.rivers_post.code_post = 9386 
	)p2 on ( public.rivers_post.date = p2.date_post_2 )
	/*-------------------POST  3---------------------------*/
/*inner join 
	(
	select
		public.rivers_post.level_w as post_3,
		public.rivers_post.date as date_post_3
	from
		public.rivers_post
	where
		public.rivers_post.code_post = 9396 
	)p3 on ( public.rivers_post.date = p3.date_post_3 )*/
	/*-------------------POST  4---------------------------*/
inner join 
	(
	select
		public.rivers_post.level_w as post_4,
		public.rivers_post.date as date_post_4
	from
		public.rivers_post
	where
		public.rivers_post.code_post = 9388 
	)p4 on ( public.rivers_post.date = p4.date_post_4 )
	/*-------------------POST  5---------------------------*/
inner join 
	(
	select
		public.rivers_post.level_w as post_5,
		public.rivers_post.date as date_post_5
	from
		public.rivers_post
	where
		public.rivers_post.code_post = 9560 
	)p5 on ( public.rivers_post.date = p5.date_post_5 )
	/*-------------------POST  6---------------------------*/
inner join 
	(
	select
		public.rivers_post.level_w as post_6,
		public.rivers_post.date as date_post_6
	from
		public.rivers_post
	where
		public.rivers_post.code_post = 9499 
	)p6 on ( public.rivers_post.date = p6.date_post_6 )
	/*-------------------POST  7---------------------------*/
inner join 
	(
	select
		public.rivers_post.level_w as post_7,
		public.rivers_post.date as date_post_7
	from
		public.rivers_post
	where
		public.rivers_post.code_post = 9392 
	)p7 on ( public.rivers_post.date = p7.date_post_7 )
	/*-------------------POST  8---------------------------*/
inner join 
	(
	select
		public.rivers_post.level_w as post_8,
		public.rivers_post.date as date_post_8
	from
		public.rivers_post
	where
		public.rivers_post.code_post = 9389 
	)p8 on ( public.rivers_post.date = p8.date_post_8 )
	/*-------------------POST  9---------------------------*/
inner join 
	(
	select
		public.rivers_post.level_w as post_9,
		public.rivers_post.date as date_post_9
	from
		public.rivers_post
	where
		public.rivers_post.code_post = 9523 
	)p9 on ( public.rivers_post.date = p9.date_post_9 )	
	/*-------------------POST  10---------------------------*/
inner join 
	(
	select
		public.rivers_post.level_w as post_10,
		public.rivers_post.date as date_post_10
	from
		public.rivers_post
	where
		public.rivers_post.code_post = 9390 
	)p10 on ( public.rivers_post.date = p10.date_post_10 )
	/*-------------------POST  11---------------------------*/ 
inner join 
	(
	select
		public.rivers_post.level_w as post_11,
		public.rivers_post.date as date_post_11
	from
		public.rivers_post
	where
		public.rivers_post.code_post = 9397 
	)p11 on ( public.rivers_post.date = p11.date_post_11 ) 
where
	public.rivers_post.code_post <> 9387
order by
	date asc
