echo " "
echo " "
echo -e "USER LOGIN \n\n"
curl --location --request POST 'http://127.0.0.1:8000/api/auth/login/' \
--form 'username=admin' \
--form 'password=moosa123'
echo " "
echo " " 

echo -e "RETRIEVING ALL TASKS FOR USER\n\n"
curl --location --request GET 'http://127.0.0.1:8000/api/task' \
--header 'Authorization: Token ba2d4f068e615f3ed9f484f828faefa81b7a9c80'
echo " " 
echo " " 
echo -e "RETRIEVING ALL COMPLETED TASKS FOR USER\n\n"
curl --location --request GET 'http://127.0.0.1:8000/api/task?status=1' \
--header 'Authorization: Token ba2d4f068e615f3ed9f484f828faefa81b7a9c80'
echo " " 
echo " " 
echo -e "RETRIEVING ALL TASKS IN A CATEGORY FOR A USER\n\n"
curl --location --request GET 'http://127.0.0.1:8000/api/task?category=9' \
--header 'Authorization: Token ba2d4f068e615f3ed9f484f828faefa81b7a9c80'
echo " " 
echo " " 

echo -e "USER CREATES NEW TASK\n\n"
curl --location --request POST 'http://127.0.0.1:8000/api/task' \
--header 'Authorization: Token ba2d4f068e615f3ed9f484f828faefa81b7a9c80' \
--form 'title=demo1' \
--form 'description=demodesc' \
--form 'category=9' \
--form 'due_date=2020-12-22 09:15:32'

echo " " 
echo " " 
echo -e "CREATE NEW CATEGORY \n\n"
curl --location --request POST 'http://127.0.0.1:8000/api/category' \
--header 'Authorization: Token ba2d4f068e615f3ed9f484f828faefa81b7a9c80' \
--form 'name=demo_category2'
echo " " 
echo " " 
echo -e "VIEW ALL CATEGORIES CREATED BY USER \n\n"
curl --location --request GET 'http://127.0.0.1:8000/api/category' \
--header 'Authorization: Token ba2d4f068e615f3ed9f484f828faefa81b7a9c80'
echo " " 
echo " " 
echo -e "UPDATE TASK ID 44 TO COMPLETED \n\n"
curl --location --request PATCH 'http://127.0.0.1:8000/api/task/44' \
--header 'Authorization: Token ba2d4f068e615f3ed9f484f828faefa81b7a9c80' \
--form 'status=1'

echo " " 
echo " " 
echo -e "SEARCH FOR TASK WITH 'DEMO' IN TITLE OR DESC \n\n"
curl --location --request GET 'http://127.0.0.1:8000/api/search?search=demo' \
--header 'Authorization: Token ba2d4f068e615f3ed9f484f828faefa81b7a9c80'



