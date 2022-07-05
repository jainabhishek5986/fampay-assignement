# fampay-assignment
FamPay Assignment

#How to Setup

    git clone https://github.com/jainabhishek5986/fampay-assignment.git

    cd backend/

    docker-compose up -d --build

Server should be up and running on port 8000 for web.

You can view logs for different used services - 
    
    docker-compose logs -f 'redis'

    docker-compose logs -f 'web'

    docker-compose logs -f 'celery'

    docker-compose logs -f 'celery-beat'

    docker-compose logs -f 'es'

You must add atleast 1 Google API Key of your choice using "Add API Keys" in below postman collection
https://www.getpostman.com/collections/7130d5a35d0e7bb7a5fe

You can configure following things in the settings file - 

"SEARCH_QUERY" - Query used for youtube search

"INTERVAL" - Regular Interval at which you wish to call the cron task.

"MAX_RESULTS" - Max results you want to fetch from Youtube.

"REST_FRAMEWORK.PAGE_SIZE" - Page count for Paginated Response.

![](https://github.com/jainabhishek5986/fampay-assignment/blob/main/backend/images/Add%20API%20Keys%20Postman.png)

Other APIs in the collection - 

1. Home Screen API - Gives latest fetched videos in reverse chronological order.

![](https://github.com/jainabhishek5986/fampay-assignment/blob/main/backend/images/Home%20Screen%20API%20Postman.png)

2. Search DB API - API for Searching in Database using Elastic Search - 

![](https://github.com/jainabhishek5986/fampay-assignment/blob/main/backend/images/Search%20API%20Postman.png)

Or You can directly visit - http://127.0.0.1:8000/youtube/home - to check the response. 


Thank you !! :D