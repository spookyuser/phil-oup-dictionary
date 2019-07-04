# Dictionary scrape

This scrapes the [Oxford dictionary of Philosophy](https://oxfordreference.com/view/10.1093/acref/9780198735304.001.0001/acref-9780198735304) for dictionary terms so they are searchable quickly because their site literally takes minutes to search for a single word. 

This can be used on scrapinghub. But it does use 17 threads or whatever so that means it logs into the univeristy website 17 times for auth because each thread saves it's own cookies. Though I think it would be possible to call one auth request and then go to the dictionary, I could not get init_request to work. 

Also you need to add credentials. 