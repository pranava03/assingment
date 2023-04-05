from flask import Flask
from flask_restful import Resource, Api, abort, reqparse
from flask_restful import fields, marshal_with
from flask_mongoengine import MongoEngine

app = Flask(__name__)
api = Api(app)
app.config['MONGODB_SETTINGS'] = {
    "db" : "users",
    "host" : "localhost",
    "port" : 27017
}
db = MongoEngine()
db.init_app(app)

# mongoDB Connectivity

#try:
#    mongo = pymongo.MongoClient(
#        host = "localhost",
#        port = 27017,
#        serverSelectionTimeoutMS = 1000         
#    )
#    db = mongo.company
#    mongo.server_info()
#except : 
#    print("Error - Cannot connect to db")

##############################

class users(db.Document):
    _id = db.IntField()
    task = db.StringField(requried = True)
    summary = db.StringField(requried = True)

todos = {
    1 : {"task" : "write hello World Program", "summary" : "write  the code using python."},
     }

task_post_args = reqparse.RequestParser()
task_post_args.add_argument("task", type=str, required=True)
task_post_args.add_argument("summary", type=str, required=True)

task_put_args = reqparse.RequestParser()
task_put_args.add_argument("task", type=str)
task_put_args.add_argument("summary", type=str)


resource_fields = {
    "_id" : fields.Integer,
    "task" :fields.String,
    "summary":fields.String
}

class  ToDoList(Resource):
    def get(self):
        tasks = users.objects.get()
        todos = {}
        for task in tasks:
            todos[task.id] = {"task" : task.task, "summary" : task.summary}
        return task    

class ToDo(Resource):
    @marshal_with(resource_fields)
    def get(self, todo_id):
        task = users.objects.get(_id = todo_id)
        if not task:
            abort(404, message = "Could not find task with that id")
        return task
    
    @marshal_with(resource_fields)
    def post(self, todo_id):
        args = task_post_args.parse_args()
        todo = users(_id=todo_id, task = args["task"], summary = args["summary"]).save()
        id_ = todo_id
        return{"id" : str(id_)}, 201
    
    def delete(self, todo_id):
        users.objects.get(_id = todo_id).delete()
        return "task deleted!",204

    @marshal_with(resource_fields)
    def put(self, todo_id):
        args = task_put_args.parse_args()
        if args["task"]:
            users.objects.get(_id = todo_id).update(task = args["task"])
        if args["summary"]:
            users.objects.get(_id = todo_id).update(task = args["summary"])
        return "{} updated!".format(todo_id),200


api. add_resource(ToDo, '/todos/<int:todo_id>')
api. add_resource(ToDoList, '/todos')

if __name__ == "__main__" :
    app.run(port = 80, debug = True)
