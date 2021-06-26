from flask import Response, render_template
from task_init import app   
import task_generator

def streamtemplate(templatename, **context):
    app.update_template_context(context)
    t = app.jinja_env.get_template(templatename)
    rv = t.stream(context)
    rv.enable_buffering(5)
    return rv

@app.route('/', methods=['GET'])
def index():
    return render_template('producer.html')

@app.route('/task', methods=['POST'])
def task():
    print("producetasks ...")
    return Response(streamtemplate()
if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True)
