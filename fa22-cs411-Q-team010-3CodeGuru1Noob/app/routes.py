""" Specifies routing for the application"""
from flask import render_template, request, jsonify
from app import app
from app import database as db_helper

@app.route("/delete/<int:userid>", methods=['GET','POST'])
def delete(userid):
    """ recieved post requests for entry delete """
    print("11")
    if request.method == 'POST':
        try:
            print(userid)
            db_helper.remove_task_by_id(userid)
            result = {'success': True, 'response': 'Removed task'}
        except:
            result = {'success': False, 'response': 'Something went wrong'}
        return jsonify(result)

    else:
        return 'GET'
    # try:
    #     db_helper.remove_task_by_id(itemId)
    #     result = {'success': True, 'response': 'Removed task'}
    # except:
    #     result = {'success': False, 'response': 'Something went wrong'}

    # return jsonify(result)





@app.route("/")
def homepage():
    """ returns rendered homepage """
    items = db_helper.fetch_todo()
    return render_template("index.html", items=items)

@app.route("/adv1", methods=['POST'])
def adv1():
    items = db_helper.adv1_helper()
    return render_template("adv1.html", items=items)

@app.route('/adv2', methods=['GET', 'POST'])
def recipe_statistics():
    items = db_helper.adv2_helper()
    return render_template('adv2.html', items=items)






@app.route('/hardlv', methods=['GET', 'POST'])
def hardlv():
    items = db_helper.hardlv_helper()
    return render_template('hardlv.html', items=items)

@app.route('/callv', methods=['GET', 'POST'])
def callv():
    items = db_helper.callv_helper()
    return render_template('callv.html', items=items)

@app.route("/search", methods=['GET'])
def search_recipe():
    """search recipe by keyword, if the keyword exist in title, subtitle, source, intro, the recipe will be shown in search result.
    """
    return render_template('index.html', recipes=[])


@app.route("/<keyword>", methods=['POST'])
def show_search_recipe(keyword):
    """search recipe by keyword, if the keyword exist in title, subtitle, source, intro, the recipe will be shown in search result.
    """
    items = db_helper.search_helper(keyword)
    # print(search_res)
    return render_template('search.html', items=items)

@app.route("/trigger_enable", methods=['GET', 'POST'])
def create_trigger():
    flag = db_helper.trigger_create_helper()
    if flag is True:
        return "Create trigger successfully"
    else:
        return "Trigger already exists"


@app.route("/trigger_disable", methods=['GET', 'POST'])
def delete_trigger():
    flag = db_helper.trigger_delete_helper()
    if flag is True:
        return "Delete trigger successfully"
    else:
        return "Trigger does not exist"


@app.route("/trigger", methods=['GET', 'POST'])
def list_trigger():
    items = db_helper.trigger_list_helper()

    return render_template('easy_recipe.html', items=items)

@app.route("/create", methods=['POST'])
def create():
    """ recieves post requests to add new task """
    data = request.get_json()
    print(data)
    title = data['title']
    cookmin = data['cookmin']
    db_helper.insert_new_recipe(title, cookmin)
    result = {'success': True, 'response': 'Done'}
    return jsonify(result)

@app.route("/editUser", methods=['POST'])
def update():
    """ recieved post requests for entry updates """
    data = request.get_json()
    # print(data)
    recipe_id = data['recipe_id']
    new_title = data['title']
    db_helper.update_recipe_title(recipe_id, new_title)
    result = {'success': True, 'response': 'Done'}
    return jsonify(result)