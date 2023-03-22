from app import db
def fetch_todo() -> dict:
    '''
    user_list = [
        {
            "account_id": 1,
            "password": "123"
        },
        {
            "account_id": 2,
            "password": "1233"
        }
    ]
    '''
    user_list = []
    conn = db.connect()
    results = conn.execute("SELECT recipe_id,title,cook_min FROM Recipe;").fetchall()
    conn.close()
    # print([x for x in results])
    for result in results:
        item = {
            "recipe_id": result[0],
            "title": result[1],
            "cook_min": result[2],

        }
        user_list.append(item)

    return user_list


def remove_task_by_id(task_id: int) -> None:
    conn = db.connect()
    # print("1")
    query = 'Delete From Recipe where recipe_id={};'.format(task_id)
    conn.execute(query)
    conn.close()


def update_status_entry(task_id: int, text: str) -> None:
    pass


def update_user_pwd(id: int, pwd: str) -> None:
    conn = db.connect()
    sql = 'update Account set password = "{}" where account_id = "{}"'.format(pwd, id)
    conn.execute(sql)
    conn.close()



def adv1_helper():
    adv1_list = []
    conn = db.connect()
    query = 'Select r.recipe_id,r.title,sum(calories * min_qty) as total_calories From Recipe r natural join Quantity q natural join Ingredient i Group by r.recipe_id Having sum(calories * min_qty) < 500 and sum(calories * min_qty) >0 Limit 15;'
    results = conn.execute(query)
    conn.close()
    for result in results:
        item = {
            "recipe_ID": result[0],
            "recipe_title": result[1],
            "calories": result[2]
        }
        adv1_list.append(item)
    return adv1_list

def adv2_helper():
    conn = db.connect()
    cate_lower = 'cheese'
    query = 'select category, count(title) as recipe_number from Recipe natural join Contain natural join Ingredient where lower(category) != "{}" group by category;'.format(
        cate_lower)
    query_res = conn.execute(query)
    search_res = []
    for res in query_res:
        item = {'category': res[0], 'num_noncheese': res[1]}
        search_res.append(item)
    return search_res

def search_helper(keyword: str):
    conn = db.connect()
    # keyword = request.form.get('keyword')
    # keyword = request.args.get('tid')
    lower_keyword = keyword.lower()
    query = 'select recipe_id, title, prep_min, cook_min from Recipe where lower(title) like "%%{}%%" or lower(subtitle) like "%%{}%%" or lower(source) like "%%{}%%" or lower(intro) like "%%{}%%" limit 15;'.format(
        lower_keyword, lower_keyword, lower_keyword, lower_keyword)
    query_result = conn.execute(query)
    search_res = []
    for result in query_result:
        item = {
            "recipe_ID": result[0],
            "recipe_title": result[1],
            "prep_time": result[2],
            "cook_time": result[3]}
        search_res.append(item)
    return search_res


def hardlv_helper():
    hardlv_list  = []
    conn = db.connect()
    query = 'Select * From NewTable;'
    results = conn.execute(query)
    conn.close()
    for result in results:
        item = {
            "recipe_ID": result[0],
            "recipe_title": result[1],
            "hardlevel": result[2]
        }
        hardlv_list.append(item)
    return hardlv_list


def callv_helper():
    callv_list  = []
    conn = db.connect()
    query = 'Select * From NewTable2;'
    results = conn.execute(query)
    conn.close()
    for result in results:
        item = {
            "recipe_ID": result[0],
            "recipe_title": result[1],
            "callv": result[2]
        }
        callv_list.append(item)
    return callv_list




def trigger_create_helper():
    conn = db.connect()
    sql = r'''create trigger IsEasy after insert on Recipe for each row
     begin
        set @cookmin = (select cook_min from Recipe where recipe_id = NEW.recipe_id);

        if @cookmin < 20 then
           insert into Easy_recipe values (NEW.recipe_id, NEW.cook_min, NEW.title);
                end if;
     end;'''

    try:
        conn.execute(sql)
    except:
        return False
    finally:
        conn.close()
    return True


def trigger_delete_helper():
    conn = db.connect()
    sql = 'DROP TRIGGER db.IsEasy;'

    try:
        conn.execute(sql)
    except:
        return False
    finally:
        conn.close()
    return True

def trigger_list_helper():
    conn = db.connect()
    sql = 'select recipe_id, title, cook_min from Easy_recipe;'
    query_result = conn.execute(sql)
    search_res = []
    for result in query_result:
        item = {
            "recipe_id": result[0],
            "title": result[1],
            "cook_min": result[2]}
        search_res.append(item)
    conn.close()
    return search_res

def insert_new_recipe(title: str, cookmin: str) -> None:

    conn = db.connect()
    sql = 'select max(recipe_id) from Recipe'
    res = conn.execute(sql).fetchall()
    recipe_id_temp = res[-1][0]
    sql = 'select * from Recipe where title = "{}"'.format(title)
    query_results = conn.execute(sql).fetchall()
    if len(query_results):
        return 'duplicate recipe'
    sql = 'insert into Recipe(recipe_id, title, cook_min) values({}, "{}", "{}");'.format(recipe_id_temp+1, title, cookmin)
    conn.execute(sql)
    conn.close()
    # login.html not create
    
def update_recipe_title(id: int, title: str) -> None:
    conn = db.connect()
    sql = 'update Recipe set title = "{}" where recipe_id = "{}"'.format(title, id)
    conn.execute(sql)
    conn.close()